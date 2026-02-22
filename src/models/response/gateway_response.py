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