from fastapi import FastAPI
from app.api.routes import router as api_router
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Initialize any resources here if needed
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Cleanup resources here if needed
    pass

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))