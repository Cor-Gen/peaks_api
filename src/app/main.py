from fastapi import FastAPI, Query
from app.db import database, Peak
from app.backend import routes


# Fast API
app = FastAPI(title = "FastAPI, Docker, and Traefik")

@app.get("/")
async def root():
    return {"message": "Hello from peaks api!"}

# mandatory to connect to the database with the API
@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()

# mandatory to disconnect from database once finished
@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

# to add our routes to the API
app.include_router(routes.router, prefix="/peaks", responses={404: {"description": "Not found"}})