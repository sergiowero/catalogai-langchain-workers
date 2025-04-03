import logging

from models.queue import DatabaseQueueMessage
from services.queues import queues
from services.supabase import supabase
from utils import dict_distinct

logger = logging.getLogger('uvicorn.error')


def handle_product_insert_event(message: DatabaseQueueMessage):
    logger.info(f'Handling product insert event for product_id: {message.row_id}')

    try:
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
            f'Created job for product_id: {message.row_id}, job_id: {data.data[0]["id"]}'
        )

        queue_message = {'job_id': data.data[0]['id'], 'product': message.curr}

        queues.rpc(
            'send',
            {
                'queue_name': 'summary_jobs',
                'sleep_seconds': 10,
                'message': queue_message,
            },
        ).execute()

        logger.info(f'Sent summary job to queue for product_id: {message.row_id}')
    except Exception as e:
        logger.error(f'Error handling product insert event: {str(e)}', exc_info=True)
        raise


def handle_product_update_event(message: DatabaseQueueMessage):
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

        queue_message = {'job_id': data.data[0]['id'], 'product': message.curr}

        queues.rpc(
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


def handle_product_delete_event(message: DatabaseQueueMessage):
    logger.info(f'Handling product delete event for product_id: {message.row_id}')

    try:
        # Add your delete handling logic here
        logger.info(
            f'Successfully handled delete event for product_id: {message.row_id}'
        )
    except Exception as e:
        logger.error(f'Error handling product delete event: {str(e)}', exc_info=True)
        raise


def handle_product_caption_insert_event(message: DatabaseQueueMessage):
    logger.info(
        f'Handling product caption insert event for product_id: {message.row_id}'
    )

    try:
        # Add your caption insert handling logic here
        logger.info(
            f'Successfully handled caption insert event for product_id: {message.row_id}'
        )
    except Exception as e:
        logger.error(
            f'Error handling product caption insert event: {str(e)}', exc_info=True
        )
        raise


def handle_product_caption_update_event(message: DatabaseQueueMessage):
    logger.info(
        f'Handling product caption update event for product_id: {message.row_id}'
    )

    try:
        # Add your caption update handling logic here
        logger.info(
            f'Successfully handled caption update event for product_id: {message.row_id}'
        )
    except Exception as e:
        logger.error(
            f'Error handling product caption update event: {str(e)}', exc_info=True
        )
        raise


def handle_product_caption_delete_event(message: DatabaseQueueMessage):
    logger.info(
        f'Handling product caption delete event for product_id: {message.row_id}'
    )

    try:
        # Add your caption delete handling logic here
        logger.info(
            f'Successfully handled caption delete event for product_id: {message.row_id}'
        )
    except Exception as e:
        logger.error(
            f'Error handling product caption delete event: {str(e)}', exc_info=True
        )
        raise


def handle_product_embedding_insert_event(message: DatabaseQueueMessage):
    logger.info(
        f'Handling product embedding insert event for product_id: {message.row_id}'
    )

    try:
        # Add your embedding insert handling logic here
        logger.info(
            f'Successfully handled embedding insert event for product_id: {message.row_id}'
        )
    except Exception as e:
        logger.error(
            f'Error handling product embedding insert event: {str(e)}', exc_info=True
        )
        raise


def handle_product_embedding_update_event(message: DatabaseQueueMessage):
    logger.info(
        f'Handling product embedding update event for product_id: {message.row_id}'
    )

    try:
        # Add your embedding update handling logic here
        logger.info(
            f'Successfully handled embedding update event for product_id: {message.row_id}'
        )
    except Exception as e:
        logger.error(
            f'Error handling product embedding update event: {str(e)}', exc_info=True
        )
        raise


def handle_product_embedding_delete_event(message: DatabaseQueueMessage):
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
    ('INSERT', 'product_captions'): handle_product_caption_insert_event,
    ('UPDATE', 'product_captions'): handle_product_caption_update_event,
    ('DELETE', 'product_captions'): handle_product_caption_delete_event,
    ('INSERT', 'product_embeddings'): handle_product_embedding_insert_event,
    ('UPDATE', 'product_embeddings'): handle_product_embedding_update_event,
    ('DELETE', 'product_embeddings'): handle_product_embedding_delete_event,
}
