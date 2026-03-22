from fastapi import APIRouter, HTTPException

from src.models.request.gateway_request import GatewayCreateRequest
from src.models.response.responses import GatewayReadingsResponse, GatewayResponse
from src.repository.db_repository import GatewayRepo
from src.service.gateway_service import GatewayService


gateway_router = APIRouter(prefix='/gateways', tags=['Gateways'])

gateway_repo = GatewayRepo()
gateway_service = GatewayService()


@gateway_router.post("/", response_model=GatewayResponse)
def create_gateway(paylaod: GatewayCreateRequest):
    print("request received", GatewayCreateRequest)
    existing = gateway_repo.get_by_imei(paylaod.imei)
    if existing:
        raise HTTPException(status_code=400, detail="Gateway already exists")
    gateway = gateway_repo.save(
        imei=paylaod.imei,
        location=paylaod.location
    )
    return gateway

@gateway_router.get("/{gateway_id}", response_model=GatewayResponse)
def get_gateway_by_id(gateway_id: int):
    gateway = gateway_repo.get_by_id(gateway_id)
    if not gateway:
        raise HTTPException(status_code=404, detail="Gateway not found")

    return gateway


@gateway_router.get("/imei/{imei}", response_model=GatewayResponse)
def get_gateway_by_imei(imei: str):
    gateway = gateway_repo.get_by_imei(imei)
    if not gateway:
        raise HTTPException(status_code=404, detail="Gateway not found")

    return gateway

@gateway_router.get("/imei/{imei}", response_model=GatewayResponse)
def get_gateway_by_imei(imei: str):
    gateway = gateway_repo.get_by_imei(imei)
    if not gateway:
        raise HTTPException(status_code=404, detail="Gateway not found")

    return gateway

@gateway_router.post("/readings", response_model=list[GatewayReadingsResponse])
def get_readings_from_gateway_ids(payload: list[int]):
    if not payload:
        raise HTTPException(status_code=400, detail="gateway ids payload cannot be empty")

    result = gateway_service.get_readings_from_gateway_ids(payload)

    if not result:
        raise HTTPException(status_code=404, detail="No gateways/devices found for provided ids")

    return result

@gateway_router.get("/", response_model=list[GatewayResponse])
def get_all_gateways():
    """Fetches all registered gateways."""
    gateways = gateway_repo.get_all_gateways()
    # If no gateways exist, return an empty list (standard REST behavior)
    return gateways