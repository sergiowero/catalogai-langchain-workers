import uuid
from enum import Enum

from pydantic import BaseModel
from services import supabase


class JobStatus(str, Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'


class Job(BaseModel):
    id: int
    owner_id: uuid.UUID
    product_id: int
    status: JobStatus
    job_type: str

    @staticmethod
    def fetchById(id: int) -> 'Job':
        response = supabase.table('jobs').select('*').eq('id', id).execute()

        return Job.model_validate(response.data[0])

    @staticmethod
    def updateStatus(id: int, status: JobStatus):
        supabase.table('jobs').update({'status': status}).eq('id', id).execute()
