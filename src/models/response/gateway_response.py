from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GatewayResponse(BaseModel):
    id: int
    imei: str
    location: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class DeviceResponse(BaseModel):
    id : int
    label: str
    location: str
    gateway_id: int
    no_of_devices: Optional[int]
    hardware_model: str
    device_no: Optional[str]
    device_type: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True