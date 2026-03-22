from datetime import date, time
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


class MetricInput(BaseModel):
    name: str    # e.g., "Vr"
    value: float # e.g., 231.4
    unit: str    # e.g., "V"

class AddReadingRequest(BaseModel):
    device_id: int
    metrics: list[MetricInput] # Accept a list here
    timestamp: str             # Format: "2026-03-08/11:50:10"
    quality_flag: int


class ShiftDetails(BaseModel):
    name: str
    start_time: time
    end_time: time

class DeviceFilterRequest(BaseModel):
    device_ids: list[int]
    filter_type: str # "Shift" or "range"
    start_date: date
    end_date: date
    shift_details: Optional[ShiftDetails]