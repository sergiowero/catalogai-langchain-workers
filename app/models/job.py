import uuid
from enum import Enum

from pydantic import BaseModel

from app.services.supabase import supabase


class JobStatus(str, Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'


class JobType(str, Enum):
    SUMMARY = 'summary'
    EMBEDDINGS = 'embeddings'
    CAPTIONS = 'captions'


class JobData(BaseModel):
    owner_id: uuid.UUID
    product_id: int
    status: JobStatus
    job_type: str


class Job(JobData):
    id: int

    @staticmethod
    def fetchById(id: int) -> 'Job':
        response = (
            supabase.table('jobs').select('*').eq('id', id).limit(1).single().execute()
        )

        return Job.model_validate(response.data)

    @staticmethod
    def updateStatus(id: int, status: JobStatus):
        supabase.table('jobs').update({'status': status}).eq('id', id).execute()

    @staticmethod
    def insert(data: JobData) -> 'Job':
        res = supabase.table('jobs').insert(data.model_dump(mode='json')).execute()
        return Job.model_validate(res.data[0])
