from fastapi import FastAPI
from api.endpoints import router

app = FastAPI()

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "API for querying BigQuery articles"}