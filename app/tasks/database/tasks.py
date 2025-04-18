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

from app.celeryapp import celery
from app.models.webhook import DatabaseWebhookPayload
from app.utils import dict_distinct

logger = logging.getLogger('uvicorn.error')


@celery.task(name='database.webhook')
def process_webhook(params: dict):
    payload = DatabaseWebhookPayload.model_validate(params)

    logger.info(f'Processing webhook event: {payload.type} - {payload.table}')

    try:
        logger.info(
            f'Successfully processed database webhook {payload.type} - {payload.table}'
        )

        handler_func = handlers_table.get((payload.type, payload.table))

        if handler_func is None:
            logger.error(
                f'No handler found for message type {payload.type} and table {payload.table}'
            )
            raise ValueError(
                f'Unknown message type {payload.type} and table {payload.table}'
            )

        handler_func.delay(payload.model_dump())
        logger.info(
            f'Successfully processed database webhook {payload.type} - {payload.table}'
        )

    except Exception as e:
        logger.error(
            f'Error processing webhook {payload.type} - {payload.table}: {str(e)}',
            exc_info=True,
        )
        raise


@celery.task(name='database.product.insert')
def handle_product_insert_event(params: dict):
    payload = DatabaseWebhookPayload.model_validate(params)
    logger.info(f'Handling product insert event for product_id: {payload.record["id"]}')

    try:
        celery.send_task('product.full', kwargs={'params': payload.record})

        logger.info(f'Sent summary job to queue for product_id: {payload.record["id"]}')
    except Exception as e:
        logger.error(f'Error handling product insert event: {str(e)}', exc_info=True)
        raise


@celery.task(name='database.product.update')
def handle_product_update_event(params: dict):
    payload = DatabaseWebhookPayload.model_validate(params)
    logger.info(f'Handling product update event for product_id: {payload.record["id"]}')

    try:
        diff_found = dict_distinct(payload.record, payload.old_record)

        if diff_found is False:
            logger.info(
                f'No significant changes found in product update for product_id: {payload.record["id"]}'
            )
            return

        celery.send_task('product.full', kwargs={'params': payload.record})

    except Exception as e:
        logger.error(f'Error handling product update event: {str(e)}', exc_info=True)
        raise


@celery.task(name='database.product.delete')
def handle_product_delete_event(params: dict):
    payload = DatabaseWebhookPayload.model_validate(params)
    logger.info(f'Handling product delete event for product_id: {payload.record["id"]}')

    try:
        # Add your delete handling logic here
        logger.info(
            f'Successfully handled delete event for product_id: {payload.record["id"]}'
        )
    except Exception as e:
        logger.error(f'Error handling product delete event: {str(e)}', exc_info=True)
        raise


handlers_table = {
    ('INSERT', 'products'): handle_product_insert_event,
    ('UPDATE', 'products'): handle_product_update_event,
    ('DELETE', 'products'): handle_product_delete_event,
}
