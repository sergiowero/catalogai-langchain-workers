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

from models.queue import DatabaseQueueItem
from services.queues import database_events_queue_read, database_events_queue_remove
from tasks.queues.database_events_handlers import handlers_table

logger = logging.getLogger('uvicorn.error')


def run(params: dict):
    logger.info('Starting database event queue processing')
    items = database_events_queue_read(10)

    if not items:
        logger.info('No items found in the database event queue')
        return

    logger.info(f'Found {len(items)} items in the database event queue')

    for item in items:
        process_single_event(item)


def process_single_event(item: DatabaseQueueItem):
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

        logger.info(f'Starting handler execution for event {item.msg_id}')
        handler_func(message)
        logger.info(f'Successfully processed event {item.msg_id}')
        logger.info(f'Removing event {item.msg_id} from queue')
        database_events_queue_remove(item.msg_id)
    except Exception as e:
        logger.error(f'Error processing event {item.msg_id}: {str(e)}', exc_info=True)
        raise
