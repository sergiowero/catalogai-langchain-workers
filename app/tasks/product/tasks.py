import logging

from pydantic import BaseModel

from app.celeryapp import celery
from app.models.job import Job, JobData, JobStatus
from app.models.product import Product, ProductEmbedding, ProductEmbeddingData
from app.services.embeddings import generate_embedding
from app.services.summarize import sumarize_product

logger = logging.getLogger('uvicorn.error')


class SummarizeParams(BaseModel):
    product_id: int


class EmbeddingsParams(BaseException):
    product_embeddings_ids: list[int]


@celery.task(bind=True, name='product.summarize')
def summarize(self, params: dict):
    try:
        params = SummarizeParams.model_validate(params)

        product = Product.fetchById(params.product_id)
        job = Job.insert(
            JobData(
                product_id=product.id,
                owner_id=product.owner_id,
                job_type='summary',
                status=JobStatus.PROCESSING,
            )
        )

        logger.info(f'Creating summary for: {job.product_id} for job: {job.job_id}')

        message = sumarize_product(product, [])
        logger.debug(
            f'Summary: {message} for product: {product.id} for job {job.job_id}'
        )

        # validate before insertion
        product_embedding = ProductEmbeddingData.model_validate(
            {
                'owner_id': product.owner_id,
                'product_id': product.id,
                'content': message.content,
                'embedding': None,
                'metadata': {
                    'job_id': job.job_id,
                    'optimizer_type': message.type,
                    'optimiser_request_id': message.id,
                    'task_execution_id': self.request.id,
                },
            }
        )

        product_embedding = ProductEmbedding.insert(product_embedding)
        Job.updateStatus(job.job_id, JobStatus.COMPLETED)

    except Exception as e:
        logger.error(
            f'Error creating summary for product: {job.product_id} for job: {job.job_id} with eror: {e}',
            exc_info=True,
        )
        Job.updateStatus(job.job_id, JobStatus.FAILED)
        raise


@celery.task(bind=True, name='product.embeddings_batch')
def embeddings_batch(self, params: dict):
    try:
        params = EmbeddingsParams.model_validate(params)

        product_embeddings = ProductEmbedding.fetchMany(params.product_embeddings_ids)

        product_ids = [pe.product_id for pe in product_embeddings]

        logger.info(f'Creating embeddings for: {product_ids}')

        embeddings = generate_embedding(
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
