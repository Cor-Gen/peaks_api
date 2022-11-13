from fastapi import APIRouter, HTTPException
from app.db import Peak
from asyncpg import exceptions as asyncpg_exc
from ormar import exceptions as ormar_exc
from ormar import and_
from typing import List, Union


router = APIRouter()

@router.get("/peaks/", response_model = List[Peak])
async def get_peaks(lat_min: float = -90,
                    lat_max: float = 90,
                    lon_min: float = -180,
                    lon_max: float = 180):
    return await Peak.objects.filter(and_(lat__gte = lat_min),
                                     and_(lat__lte = lat_max),
                                     and_(lon__gte = lon_min),
                                     and_(lon__lte = lon_max)).all()

@router.get("/peaks/{id}")
async def get_peak(id: int):
    try:
        peak_db = Peak.objects.get(id = id)
        return await peak_db
    except ormar_exc.NoMatch:
        raise HTTPException(status_code = 404, detail = "Peak not found.")

@router.post("/peaks/", response_model = Peak, status_code = 201)
async def create_peak(peak: Peak):
    try:
        new_peak = await peak.save()
        return new_peak
    except asyncpg_exc.UniqueViolationError:
        raise HTTPException(status_code = 400, detail = "Peak already exist(s).")

@router.put("/peaks/{id}", response_model = Peak)
async def update_peak(id: int, peak: Peak):
    try:
        item_db = await Peak.objects.get(pk = id)
        update = peak.dict()
        update.pop("id")
        return await item_db.upsert(id = id, **update)
    except ormar_exc.NoMatch:
        raise HTTPException(status_code = 404, detail = "Peak not found.")

@router.delete("/peaks/{id}")
async def delete_peak(id: int):
    try:
        peak_db = await Peak.objects.get(id = id)
        await peak_db.delete()
        return peak_db
    except ormar_exc.NoMatch:
        raise HTTPException(status_code = 404, detail = "Peak not found.")
