import subprocess

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.repository.db_repository import GatewayRepo
from src.mqtt.mqtt_service import MqttService
from src.repository.raw_mqtt_event_repository import RawMqttEventRepository
from src.mqtt import mqtt_client
from src.db.database import Base, engine
from src.router.readings_router import readings_router as readings_router
from src.router.device_router import device_router as device_router
from src.router.gateway_router import gateway_router as gateway_router

app = FastAPI()
raw_mqtt_event_repository = RawMqttEventRepository()
gateway_repo = GatewayRepo()

mqtt_service = MqttService(raw_mqtt_event_repository, gateway_repo)
mqtt_client = mqtt_client.MqttClient(mqtt_service)
MQTT_LISTENER_ENABLED = True

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add any other origins (ports) you use
]

@app.get("/")
async def root():
    return {"message": "FastAPI with Poetry 🚀 \n "
    "MQTT listener running in background thread."}

app.include_router(gateway_router)
app.include_router(device_router)
app.include_router(readings_router)


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

# 2. Add the middleware to your app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],              # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],              # Allows all headers (Content-Type, etc.)
)