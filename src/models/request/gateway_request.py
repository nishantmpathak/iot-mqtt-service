from typing import Optional

from pydantic import BaseModel, Field


class GatewayCreateRequest(BaseModel):
    imei: str = Field(..., min_length=10, max_length=50)
    location: Optional[str] = None


class CreateDeviceRequest(BaseModel):
    label: str
    location: str
    gateway_id: int
    hardware_model: str
    device_type: str
    is_active: bool