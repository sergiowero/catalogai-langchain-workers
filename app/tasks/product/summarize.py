import logging

from celeryapp import celery
from models.job import Job
from models.product import Product, ProductEmbedding
from models.queue import JobStatus
from pydantic import BaseModel
from services.optimizers import optimize_product_description

logger = logging.getLogger('uvicorn.error')


class SummarizeJob(BaseModel):
    job_id: int
    product_id: int


@celery.task(bind=True, name='product.summarize')
def summarize(self, params: dict):
    try:
        job = SummarizeJob.model_validate(params)
        Job.updateStatus(job.job_id, JobStatus.PROCESSING)
        logger.info(f'Creating summary for: {job.product_id} for job: {job.job_id}')
        product = Product.fetchById(job.product_id)
        message = optimize_product_description(product, [])
        logger.debug(
            f'Summary: {message} for product: {product.id} for job {job.job_id}'
        )

        # validate before insertion
        product_embedding = ProductEmbedding.model_validate(
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

        ProductEmbedding.insert(product_embedding)
        Job.updateStatus(job.job_id, JobStatus.COMPLETED)

    except Exception as e:
        logger.error(
            f'Error creating summary for product: {job.product_id} for job: {job.job_id} with eror: {e}',
            exc_info=True,
        )
        Job.updateStatus(job.job_id, JobStatus.FAILED)
        raise
