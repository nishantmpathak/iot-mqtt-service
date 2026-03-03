from fastapi import APIRouter, HTTPException

from src.models.gateway import DeviceInfo
from src.models.request.gateway_request import CreateDeviceRequest
from src.models.response.gateway_response import DeviceResponse
from src.repository.Gateway_repository import DeviceInforRepo


device_router = APIRouter(prefix='/device', tags=['Device'])

repo = DeviceInforRepo()

@device_router.post("/", response_model=DeviceResponse)
def create_device(paylaod: CreateDeviceRequest):
    print("request received", paylaod)
    db_device = DeviceInfo(**paylaod.model_dump())
    print(db_device)
    # deviceInfoEntity = DeviceInfo(
    #     label = paylaod.label,
    #     location = paylaod.location,
    #     gateway_id = paylaod.gateway_id,
    #     hardware_mode = paylaod.hardware_model,
    #     device_type = paylaod.device_type,
    #     is_active = paylaod.is_active
    # )
    deice = repo.save(db_device)
    return deice

@device_router.get("/{device_id}", response_model=DeviceResponse)
def get_device_by_id(device_id: int):
    device = repo.get_by_id(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="device not found")

    return device
