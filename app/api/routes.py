from fastapi import APIRouter, HTTPException
from app.services.embeddings import create_embedding, save_embedding_to_supabase
from app.services.queue import queue_read

router = APIRouter(prefix='/api/v1')

@router.post("/embeddings/")
async def generate_and_save_embedding(data: dict):
    try:
        # Create embedding using LangChain
        embedding = await create_embedding(data["text"])
        
        # Save embedding to Supabase
        await save_embedding_to_supabase(embedding)
        
        return {"message": "Embedding created and saved successfully", "embedding": embedding}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/jobs/")
async def get_jobs():
    try:
        # Read from the queue
        jobs = queue_read()
        
        if not jobs:
            raise HTTPException(status_code=404, detail="No jobs found")
        
        return {"jobs": jobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))