from datetime import date, datetime, time
from typing import Any, Optional, Union

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator


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

class MetricEntry(BaseModel):
    metric: str
    metric_value: Optional[float]
    metric_unit: Optional[str]

class ReadingResponse(BaseModel):
    id: int
    device_id: int
    timestamp: datetime
    created_at: datetime
    quality_flag: int
    
    readings: list[MetricEntry] = Field(validation_alias=AliasChoices("readings", "data"))

    class Config:
        from_attributes = True

    @field_validator("readings", mode="before")
    @classmethod
    def transform_dict_to_list(cls, v):
        if isinstance(v, dict):
            return [
                {"name": key, "value": val["value"], "unit": val["unit"]}
                for key, val in v.items()
            ]
        return v

class GetReadingsForDevice(BaseModel):
    device_id: int
    label: str
    location: str
    timestamp: str
    reading: Union[dict[str, Any],list[Any]]

class MetricReadingResponse(BaseModel):
    metric: str
    metric_value: float | int | str | None = None
    metric_unit: str | None = None
    
class ReadingPayloadResponse(BaseModel):
    id: int
    device_id: int
    readings: list[MetricReadingResponse]
    timestamp: datetime
    created_at: datetime
    quality_flag: int | str | None = None

    model_config = ConfigDict(from_attributes=True)

class DeviceReadingResponse(BaseModel):
    device_id: int
    label: str
    location: Optional[str] = None
    device_type: str
    is_active: bool
    latest_reading: Optional[ReadingPayloadResponse] = None

    model_config = ConfigDict(from_attributes=True)

class GatewayReadingsResponse(BaseModel):
    gateway_id: int
    imei: str
    location: Optional[str] = None
    devices: list[DeviceReadingResponse]

class FullReadingResponse(BaseModel):
    id : int
    timestamp : datetime
    readings: list[MetricReadingResponse]
    created_at: datetime
    quality_flag: int | str | None = None

class DeviceReadingResponse(BaseModel):
    device_id : int
    label : str
    location: str
    device_type: str
    is_active: bool
    formatted_readings: Optional[list[FullReadingResponse]] = None
    
    
