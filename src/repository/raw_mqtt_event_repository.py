from src.db.database import SessionLocal
from src.models.raw_mqtt_event import RawMqttEvent


class RawMqttEventRepository:

    def save(self, gateway_id: int, topic: str, payload_text: str):
        db = SessionLocal()
        print('Saving MQTT event to DB with gateway_id:', gateway_id, 'topic:', topic)
        try:
            event = RawMqttEvent(
                gateway_id=gateway_id,
                topic=topic,
                payload_text=payload_text
            )
            db.add(event)
            db.commit()
            db.refresh(event)
            return event
        finally:
            db.close()