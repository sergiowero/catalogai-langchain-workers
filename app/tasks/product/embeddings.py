"""
Product Embeddings Task Module

This module handles the generation of embeddings for product data, including text and image processing.
It manages the queue of items to process and coordinates the generation of embeddings for product descriptions
and images, storing the results in Supabase.

The main functionality is provided by the `execute` function, which processes items from the embeddings queue,
handles image captioning, product description optimization, and embedding generation.
"""

import logging

from config import config
from models.product import ProductEmbedding
from models.queue import JobStatus
from services.captioning import get_image_caption
from services.embeddings import generate_embedding
from services.optimizers import optimize_product_description
from services.queues import embeddings_queue_read, embeddings_queue_remove
from services.supabase import supabase

logger = logging.getLogger('uvicorn.error')


def run(params: dict):
    queue_items = embeddings_queue_read(params['items_to_process'])
    if queue_items is None:
        return

    supabase.table('jobs').update({'status': JobStatus.PROCESSING}).in_(
        'id', [item.message.job_id for item in queue_items]
    ).execute()

    product_embeddings: list[ProductEmbedding] = []

    for item in queue_items:
        try:
            product = item.message.product

            if config.ENABLE_IMAGE_CAPTIONS:
                image_captions = [
                    get_image_caption(image_url)
                    for image_url in item.message.product.image_urls
                ]
            else:
                image_captions = []

            logger.info(f'Processing embeddings product: {product}')

            logger.info(f'Creating optimized description for: {product.id}')
            message = optimize_product_description(product, image_captions)
            logger.debug(f'Optimization description: {message} for ')

            if message is None:
                supabase.table('jobs').update(
                    {
                        'status': JobStatus.FAILED,
                        'error_message': 'optimize_product_description: failed',
                    }
                ).eq('id', item.message.job_id).execute()
                continue

            product_embeddings.append(
                ProductEmbedding.model_validate(
                    {
                        'product_id': product.id,
                        'content': message.content,
                        'owner_id': product.owner_id,
                        'embedding': [],
                        'metadata': {
                            'job_id': item.message.job_id,
                            'optimizer_type': message.type,
                            'optimiser_request_id': message.id,
                            'queue_id': item.msg_id,
                            'product': product.model_dump(),
                        },
                    }
                )
            )
        except Exception as e:
            logger.error(f'Error processing item {item}: {e}')
            supabase.table('jobs').update(
                {'status': JobStatus.FAILED, 'error_message': str(e)}
            ).eq('id', item.message.job_id).execute()
            continue

    try:
        product_documents = [pe.content for pe in product_embeddings]
        embeddings = generate_embedding(product_documents)
        logger.debug(f'Generated embeddings: {embeddings}')

        for res, embedding in zip(product_embeddings, embeddings):
            res.embedding = embedding.values

        supabase.table('product_embeddings').insert(
            [pe.model_dump(mode='json') for pe in product_embeddings]
        ).execute()

        supabase.table('jobs').update({'status': JobStatus.COMPLETED}).in_(
            'id', [pe.metadata['job_id'] for pe in product_embeddings]
        ).execute()

    except Exception as e:
        logger.error(f'Error generating embeddings: {e}')
        supabase.table('jobs').update(
            {'status': JobStatus.FAILED, 'error_message': str(e)}
        ).in_('id', [pe.metadata['job_id'] for pe in product_embeddings]).execute()

    finally:
        for item in queue_items:
            logger.info(f'Removing item from queue: {item.msg_id}')
            embeddings_queue_remove(item.msg_id)
