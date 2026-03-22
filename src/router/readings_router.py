import json

from fastapi import APIRouter, HTTPException


from src.models.request.gateway_request import AddReadingRequest
from src.models.response.responses import ReadingResponse
from src.repository.db_repository import ReadingsRepo
from src.service.readings_service import ReadingService


readings_router = APIRouter(prefix='/readings', tags=['Readings'])

repo = ReadingsRepo()

reading_service = ReadingService(repo) 

@readings_router.post("/", response_model=ReadingResponse)
def create_readings(payload: AddReadingRequest):
    # Initialize service and repo
    
    # This will now handle the list of metrics
    try:
        reading = reading_service.add_device_readings(payload)
        reading_list =  [{'metric': metric, 'metric_value' : value['value'], 'metric_unit': value['unit']}for metric, value in reading.data.items()]
        return ReadingResponse(
        id= reading.id,
        device_id= reading.device_id,
        readings=reading_list,
        timestamp=reading.timestamp,
        created_at=reading.created_at,
        quality_flag=reading.quality_flag
    )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@readings_router.get("/{id}", response_model=ReadingResponse)
def get_device_by_id(reading_id: int):
    reading = repo.get_by_id(reading_id)

    if reading:
        print(json.dumps(reading.data, indent=2))
    if not reading:
        raise HTTPException(status_code=404, detail="device not found")
    
    reading_list =  [{'metric': metric, 'metric_value' : value['value'], 'metric_unit': value['unit']}for metric, value in reading.data.items()]
    return ReadingResponse(
        id= reading.id,
        device_id= reading.device_id,
        readings=reading_list,
        timestamp=reading.timestamp,
        created_at=reading.created_at,
        quality_flag=reading.quality_flag
    )

