from fastapi import FastAPI

from src.api.routers.endpoints import endpoints_router

app = FastAPI()

app.include_router(endpoints_router)


@app.get("/status")
def health_check():
    return {"status": "Running"}
