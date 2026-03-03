import subprocess

from fastapi import FastAPI

from src.repository.Gateway_repository import GatewayRepo
from src.mqtt.mqtt_service import MqttService
from src.repository.raw_mqtt_event_repository import RawMqttEventRepository
from src.mqtt import mqtt_client
from src.db.database import Base, engine
from src.router.device_router import device_router as device_router
from src.router.gateway_router import gateway_router as gateway_router

app = FastAPI()
raw_mqtt_event_repository = RawMqttEventRepository()
gateway_repo = GatewayRepo()

mqtt_service = MqttService(raw_mqtt_event_repository, gateway_repo)
mqtt_client = mqtt_client.MqttClient(mqtt_service)
MQTT_LISTENER_ENABLED = True

@app.get("/")
async def root():
    return {"message": "FastAPI with Poetry 🚀 \n "
    "MQTT listener running in background thread."}

app.include_router(gateway_router)
app.include_router(device_router)


@app.on_event("startup")
def create_tables():
    print("🔥 Creating tables...")
    Base.metadata.create_all(bind=engine)
    
@app.on_event("startup")
def run_migrations():
    subprocess.run(["alembic", "upgrade", "head"])

@app.on_event("startup")
def startup_event():
    if MQTT_LISTENER_ENABLED:
        print("Starting MQTT listener...")
        mqtt_client.run_mqtt_in_thread()