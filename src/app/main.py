from fastapi import FastAPI, Query
from app.db import database, Peak
from app.backend import routes


app = FastAPI(title = "FastAPI, Docker, and Traefik")

@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


app.include_router(routes.router)