import logging

from models.product import ProductEmbedding
from models.queue import JobStatus, SummarizeQueueItem
from services.optimizers import optimize_product_description
from services.queues import summary_jobs_queue_remove
from services.supabase import supabase

logger = logging.getLogger('uvicorn.error')


def run(item: SummarizeQueueItem):
    supabase.table('jobs').update({'status': JobStatus.PROCESSING}).eq(
        'id', item.message.job_id
    ).execute()

    try:
        logger.info(
            f'Creating summary for: {item.message.product.id} in response of message: {item.msg_id}'
        )
        message = optimize_product_description(
            item.message.product, item.message.image_captions
        )
        logger.debug(
            f'Optimization description: {message} for product: {item.message.product.id} in response of message: {item.msg_id}'
        )

        # validate before insertion
        product_embedding = ProductEmbedding.model_validate(
            {
                'product_id': item.message.product.id,
                'content': message.content,
                'owner_id': item.message.product.owner_id,
                'embedding': None,
                'metadata': {
                    'job_id': item.message.job_id,
                    'optimizer_type': message.type,
                    'optimiser_request_id': message.id,
                    'queue_id': item.msg_id,
                },
            }
        )

        supabase.table('product_embeddings').insert(
            product_embedding.model_dump(mode='json')
        ).execute()

        supabase.table('jobs').update({'status': JobStatus.COMPLETED}).eq(
            'id', item.message.job_id
        ).execute()

        logger.info(f'Removing summary job from queue: {item.msg_id}')
        summary_jobs_queue_remove(item.msg_id)

    except Exception as e:
        logger.error(
            f'Error creating summary for product: {item.message.product.id} in response of message: {item.msg_id}',
            exc_info=True,
        )
        supabase.table('jobs').update(
            {'status': JobStatus.FAILED, 'error_message': str(e)}
        ).eq('id', item.message.job_id).execute()
        raise
