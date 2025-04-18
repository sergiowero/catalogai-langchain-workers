import logging
import uuid
import zlib

from celery import chain
from pydantic import BaseModel

from app.celeryapp import celery
from app.models.product import (
    Product,
    ProductCaptions,
    ProductEmbedding,
)
from app.services import summarize
from app.services.captioning import get_image_caption, get_image_data
from app.services.embeddings import embed_documents

logger = logging.getLogger('uvicorn.error')


@celery.task(bind=True, name='product.full')
def product(self, params: dict):
    """
    Generate product embeddings for the given products.
    """
    logger.info(f'Processing product: {params}')
    try:
        return chain(
            summarize_rag.s(params),
            summarize_marketing.s(params),
            sumarize_save.s(params),
        )()

    except Exception as e:
        logger.error(
            f'Error generating product embeddings with error: {e}',
            exc_info=True,
        )
        raise


@celery.task(bind=True, name='product.summarize.rag')
def summarize_rag(self, params: dict):
    try:
        product = Product.model_validate(params)

        message = summarize.generate_rag_description(product)
        logger.info(f'Rag descrption for product {product.id}: {message}')
        return message

    except Exception as e:
        logger.error(
            f'Error creating summary for product: {product.id} with eror: {str(e)}',
            exc_info=True,
        )
        raise


@celery.task(bind=True, name='product.summarize.marketing')
def summarize_marketing(self, rag_description: str, params: dict):
    try:
        product = Product.model_validate(params)

        message = summarize.sumarize_marketing_description(rag_description, product)
        logger.info(f'Marketing description product {product.id}: {message}')

        return {
            'marketing': message,
            'rag': rag_description,
        }

    except Exception as e:
        logger.error(
            f'Error creating summary for product: {product.id} with eror: {str(e)}',
            exc_info=True,
        )
        raise


@celery.task(bind=True, name='product.summarize.save')
def sumarize_save(self, results: dict, params: dict):
    """
    Save the results of the summarization to the database.
    """
    try:
        product = Product.model_validate(params)

        logger.info(
            f'Saving summaries for product: {product.id} and owner: {product.owner_id}'
        )

        summarize.upsert_sumarize_results(
            results['rag'],
            results['marketing'],
            product,
        )
        logger.info(
            f'Summaries saved for product {product.id} and owner: {product.owner_id}'
        )

    except Exception as e:
        logger.error(f'Error saving summaries with error: {e}', exc_info=True)
        raise


class EmbeddingsParams(BaseException):
    product_embeddings_ids: list[int]


@celery.task(bind=True, name='product.embeddings_batch')
def embeddings_batch(self, params: dict):
    try:
        params = EmbeddingsParams.model_validate(params)

        product_embeddings = ProductEmbedding.fetchMany(params.product_embeddings_ids)

        product_ids = [pe.product_id for pe in product_embeddings]

        logger.info(f'Creating embeddings for: {product_ids}')

        embeddings = embed_documents(
            [pe.content for pe in product_embeddings if pe.content is not None]
        )
        logger.debug(f'Embeddings generated for products: {product_ids}')

        for pe, embedding in zip(product_embeddings, embeddings):
            pe.embedding = embedding.values

        ProductEmbedding.updateMany(product_embeddings)

    except Exception as e:
        logger.error(
            f'Error creating embeddings for products: {product_ids} with error: {e}',
            exc_info=True,
        )
        raise


class ImageCaptionParams(BaseModel):
    image_url: str
    product_id: int
    owner_id: uuid.UUID


@celery.task(name='product.image.captions.load')
def load_image(image_url: str):
    """
    Load image data for the given products.
    """
    logger.info(f'Loading image data for: {image_url}')
    try:
        return get_image_data(image_url)
    except Exception as e:
        logger.error(f'Error loading images with error: {e}', exc_info=True)
        raise


@celery.task(name='product.image.captions.generate')
def image_caption(image_data: bytes):
    """
    Generate image captions for the given products.
    """
    logger.info('Generating image captions ')
    try:
        return get_image_caption(image_data)
    except Exception as e:
        logger.error(f'Error generating image captions with error: {e}', exc_info=True)
        raise


@celery.task(bind=True, name='product.image.captions.save')
def save_caption(self, captions: str, params: dict):
    """
    Generate image captions for the given products.
    """

    image_caption_params = ImageCaptionParams.model_validate(params)

    logger.info(
        f'Saving image captions for product: {image_caption_params.product_id} and owner: {image_caption_params.owner_id}'
    )

    try:
        image_url_hash = zlib.adler32(
            image_caption_params.image_url.encode('utf-8')
        ) - (1 << 31)
        data = ProductCaptions.model_validate(
            {
                'product_id': image_caption_params.product_id,
                'image_url_hash': image_url_hash,
                'owner_id': image_caption_params.owner_id,
                'captions': captions,
                'metadata': {
                    'task_execution_id': self.request.id,
                },
            }
        )
        return ProductCaptions.insert(data).model_dump(mode='json')
    except Exception as e:
        logger.error(f'Error generating image captions with error: {e}', exc_info=True)
        raise


@celery.task(bind=True, name='product.image.captions')
def generate_image_caption(self, params: dict):
    """
    Generate image captions for the given products.
    """

    image_caption_params = ImageCaptionParams.model_validate(params)
    logger.info(f'Generating image captions for: {image_caption_params.image_url}')

    try:
        return chain(
            load_image.s(image_caption_params.image_url),
            image_caption.s(),
            save_caption.s(image_caption_params.model_dump(mode='json')),
        )()
    except Exception as e:
        logger.error(f'Error generating image captions with error: {e}', exc_info=True)
        raise
