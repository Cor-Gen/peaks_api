from fastapi import APIRouter, HTTPException
from app.db import Peak
from asyncpg import exceptions as asyncpg_exc
from ormar import exceptions as ormar_exc
from ormar import and_
from typing import List, Union
from copy import deepcopy


# routes for peaks_api
router = APIRouter()

@router.get("/peaks", response_model = List[Peak])
async def get_peak():
# GET all peaks.
    return await Peak.objects.all()

@router.get("/peaks/search", response_model = List[Peak])
# GET all peaks matching the search (with possibility to filter peaks within a given geographical bouding box).
async def get_peaks(name   : str = None,
                    lat_min: float = -90,
                    lat_max: float = 90,
                    lon_min: float = -180,
                    lon_max: float = 180):
    search = Peak.objects.filter(and_(lat__gte = lat_min),
                                 and_(lat__lte = lat_max),
                                 and_(lon__gte = lon_min),
                                 and_(lon__lte = lon_max))
    if name:
        search = search.filter(name = name)
    return await search.all()

@router.get("/peaks/{id}")
async def get_peak(id: int):
# GET a peak by its id.
    try:
        peak_db = Peak.objects.get(id = id)
        return await peak_db
    except ormar_exc.NoMatch:
        raise HTTPException(status_code = 404, detail = "Peak not found.")

@router.post("/peaks/", response_model = Peak, status_code = 201)
# POST a peak.
async def create_peak(peak: Peak):
    detail = {"detail": []}
    loc    = {"loc": ["body"],
              "msg": "field required",
              "type": "value_error.missing"}

    for key, value in peak.dict().items():
        if key != "id" and value == None:
            new_loc = deepcopy(loc)
            new_loc["loc"].append(key)
            detail["detail"].append(new_loc)
    if detail["detail"]:
        raise HTTPException(status_code = 422, detail = detail)
    
    try:
        new_peak = await peak.save()
        return new_peak
    except asyncpg_exc.UniqueViolationError:
        raise HTTPException(status_code = 400, detail = "Peak already exist(s).")

@router.put("/peaks/{id}", response_model = Peak)
async def update_peak(id: int, peak: Peak):
# PUT an update to a peak (partial or complete).
    try:
        item_db = await Peak.objects.get(pk = id)
        update = peak.dict(exclude_none = True)
        return await item_db.upsert(id = id, **update)
    except ormar_exc.NoMatch:
        raise HTTPException(status_code = 404, detail = "Peak not found.")

@router.delete("/peaks/{id}")
async def delete_peak(id: int):
# DELETE a peak.
    try:
        peak_db = await Peak.objects.get(id = id)
        await peak_db.delete()
        return peak_db
    except ormar_exc.NoMatch:
        raise HTTPException(status_code = 404, detail = "Peak not found.")
