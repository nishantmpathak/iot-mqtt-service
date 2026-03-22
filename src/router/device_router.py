from fastapi import APIRouter, HTTPException

from src.models.entities import DeviceInfo
from src.models.request.gateway_request import CreateDeviceRequest, DeviceFilterRequest
from src.models.response.responses import DeviceReadingResponse, DeviceResponse
from src.repository.db_repository import DeviceInforRepo
from src.service.device_service import DeviceService


device_router = APIRouter(prefix='/device', tags=['Device'])

repo = DeviceInforRepo()
service = DeviceService()

@device_router.post("/", response_model=DeviceResponse)
def create_device(paylaod: CreateDeviceRequest):
    print("request received", paylaod)
    db_device = DeviceInfo(**paylaod.model_dump())
    print(db_device)
    deice = repo.save(db_device)
    return deice

@device_router.get("/{device_id}", response_model=DeviceResponse)
def get_device_by_id(device_id: int):
    device = repo.get_by_id(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="device not found")

    return device


@device_router.post(path='/readings', response_model=list[DeviceReadingResponse])
def get_readings(payload: DeviceFilterRequest):
    return service.get_device_readings_filter(payload)
