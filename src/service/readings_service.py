from datetime import datetime
from src.models.entities import Readings
from src.models.request.gateway_request import AddReadingRequest

class ReadingService:
    def __init__(self, repo):
        self.repo = repo

    def add_device_readings(self, payload: AddReadingRequest):
        jsonb_data: dict[str, dict[any]] = {
            m.name: {"value": m.value, "unit": m.unit} 
            for m in payload.metrics
        }

        # 2. Map to SQLAlchemy Entity
        db_reading = Readings(
            device_id=payload.device_id,
            quality_flag=payload.quality_flag,
            timestamp=datetime.strptime(payload.timestamp, "%Y-%m-%d/%H:%M:%S"),
            data=jsonb_data  # Save the full dictionary here
        )

        return self.repo.save(db_reading)