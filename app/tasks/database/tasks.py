"""
Module for processing database events from the queue system.

This module handles the processing of database events that are queued for
asynchronous processing. It reads events from the database queue, processes
them using appropriate handlers, and removes them from the queue upon
successful processing or failure.

Key Features:
- Reads database events from the queue
- Processes events using table-specific handlers
- Handles errors gracefully with logging
- Removes processed events from the queue

"""

import logging

from pydantic import ValidationError

from app.celeryapp import celery
from app.models.product import ProductEmbedding
from app.models.queue import DatabaseQueueItem, DatabaseQueueMessage
from app.models.webhook import DatabaseWebhookPayload
from app.services.queues import database_events_queue_read, database_events_queue_remove
from app.services.supabase import supabase, supabase_queues
from app.utils import dict_distinct

logger = logging.getLogger('uvicorn.error')


@celery.task(name='database.event_queue')
def process_queue(params: dict):
    logger.info('Starting database event queue processing')
    items = database_events_queue_read(10)

    if not items:
        logger.info('No items found in the database event queue')
        return

    logger.info(f'Found {len(items)} items in the database event queue')

    for item in items:
        process_event.delay(item.model_dump())


@celery.task(name='database.webhook')
def process_webhook(params: dict):
    payload = DatabaseWebhookPayload.model_validate(params)

    logger.info(f'Processing webhook event: {payload.type} - {payload.table}')

    try:
        logger.info(
            f'Successfully processed database webhook {payload.type} - {payload.table}'
        )
    except Exception as e:
        logger.error(
            f'Error processing webhook {payload.type} - {payload.table}: {str(e)}',
            exc_info=True,
        )
        raise


@celery.task(name='database.event')
def process_event(params: dict):
    item = DatabaseQueueItem.model_validate(params)

    logger.info(
        f'Processing event: {item.msg_id} - {item.message.type} for table {item.message.table}'
    )
    message = item.message

    try:
        handler_func = handlers_table.get((message.type, message.table))

        if handler_func is None:
            logger.error(
                f'No handler found for message type {message.type} and table {message.table}'
            )
            raise ValueError(
                f'Unknown message type {message.type} and table {message.table}'
            )

        handler_func.delay(message.model_dump())
        logger.info(f'Successfully processed database event {item.msg_id}')
        logger.info(f'Removing event {item.msg_id} from queue')
        database_events_queue_remove(item.msg_id)
    except Exception as e:
        logger.error(f'Error processing event {item.msg_id}: {str(e)}', exc_info=True)
        raise


@celery.task(name='database.product.insert')
def handle_product_insert_event(params: dict):
    message = DatabaseQueueMessage.model_validate(params)
    logger.info(f'Handling product insert event for product_id: {message.row_id}')

    try:
        params = {'product_id': message.row_id}

        celery.send_task('product.summarize', kwargs={'params': params})

        logger.info(f'Sent summary job to queue for product_id: {message.row_id}')
    except Exception as e:
        logger.error(f'Error handling product insert event: {str(e)}', exc_info=True)
        raise


@celery.task(name='database.product.update')
def handle_product_update_event(params: dict):
    message = DatabaseQueueMessage.model_validate(params)
    logger.info(f'Handling product update event for product_id: {message.row_id}')

    try:
        diff_found = dict_distinct(message.curr, message.prev)

        if diff_found is False:
            logger.info(
                f'No significant changes found in product update for product_id: {message.row_id}'
            )
            return

        data = (
            supabase.table('jobs')
            .insert(
                {
                    'owner_id': message.curr['owner_id'],
                    'product_id': message.row_id,
                    'job_type': 'summary',
                    'status': 'pending',
                }
            )
            .execute()
        )

        logger.info(
            f'Created summary job for product_id: {message.row_id}, job_id: {data.data[0]["id"]}'
        )

        queue_message = {'job_id': data.data[0]['id'], 'product_id': message.row_id}

        supabase_queues.rpc(
            'send',
            {
                'queue_name': 'summary_jobs',
                'sleep_seconds': 10,
                'message': queue_message,
            },
        ).execute()

        logger.info(f'Sent summary job to queue for product_id: {message.row_id}')
    except Exception as e:
        logger.error(f'Error handling product update event: {str(e)}', exc_info=True)
        raise


@celery.task(name='database.product.delete')
def handle_product_delete_event(params: dict):
    message = DatabaseQueueMessage.model_validate(params)
    logger.info(f'Handling product delete event for product_id: {message.row_id}')

    try:
        # Add your delete handling logic here
        logger.info(
            f'Successfully handled delete event for product_id: {message.row_id}'
        )
    except Exception as e:
        logger.error(f'Error handling product delete event: {str(e)}', exc_info=True)
        raise


@celery.task(name='database.product.embedding.insert')
def handle_product_embedding_insert_event(params: dict):
    message = DatabaseQueueMessage.model_validate(params)
    logger.info(
        f'Handling product embedding insert event for product_id: {message.row_id}'
    )

    try:
        product_embedding = ProductEmbedding.model_validate(message.curr)

        if product_embedding.embedding is not None:
            logger.info(
                f'Product embedding already exists for product_id skipping summary job: {message.row_id}'
            )
            return

        logger.info(
            f'Successfully handled embedding insert event for product_id: {message.row_id}'
        )
    except ValidationError as ve:
        logger.error(
            f'Error validating product embedding insert event: {str(ve)}', exc_info=True
        )
        raise
    except Exception as e:
        logger.error(
            f'Error handling product embedding insert event: {str(e)}', exc_info=True
        )
        raise


@celery.task(name='database.product.embedding.update')
def handle_product_embedding_update_event(params: dict):
    message = DatabaseQueueMessage.model_validate(params)
    logger.info(f'Handling product embedding update event for id: {message.row_id}')

    try:
        diff_found = dict_distinct(message.curr, message.prev)

        if diff_found is False:
            logger.info(
                f'No significant changes found in product embedding update for id: {message.row_id}'
            )
            return

        logger.info(
            f'Successfully handled product embedding update event for id: {message.row_id}'
        )
    except Exception as e:
        logger.error(
            f'Error handling product embedding update event: {str(e)}', exc_info=True
        )
        raise


@celery.task(name='database.product.embedding.delete')
def handle_product_embedding_delete_event(params: dict):
    message = DatabaseQueueMessage.model_validate(params)
    logger.info(
        f'Handling product embedding delete event for product_id: {message.row_id}'
    )

    try:
        # Add your embedding delete handling logic here
        logger.info(
            f'Successfully handled embedding delete event for product_id: {message.row_id}'
        )
    except Exception as e:
        logger.error(
            f'Error handling product embedding delete event: {str(e)}', exc_info=True
        )
        raise


handlers_table = {
    ('INSERT', 'products'): handle_product_insert_event,
    ('UPDATE', 'products'): handle_product_update_event,
    ('DELETE', 'products'): handle_product_delete_event,
    ('INSERT', 'product_embeddings'): handle_product_embedding_insert_event,
    ('UPDATE', 'product_embeddings'): handle_product_embedding_update_event,
    ('DELETE', 'product_embeddings'): handle_product_embedding_delete_event,
}
