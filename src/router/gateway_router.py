from fastapi import APIRouter, HTTPException

from src.models.request.gateway_request import GatewayCreateRequest
from src.models.response.gateway_response import GatewayResponse
from src.repository.Gateway_repository import GatewayRepo


gateway_router = APIRouter(prefix='/gateways', tags=['Gateways'])

repo = GatewayRepo()

@gateway_router.post("/", response_model=GatewayResponse)
def create_gateway(paylaod: GatewayCreateRequest):
    print("request received", GatewayCreateRequest)
    existing = repo.get_by_imei(paylaod.imei)
    if existing:
        raise HTTPException(status_code=400, detail="Gateway already exists")
    gateway = repo.save(
        imei=paylaod.imei,
        location=paylaod.location
    )
    return gateway

@gateway_router.get("/{gateway_id}", response_model=GatewayResponse)
def get_gateway_by_id(gateway_id: int):
    gateway = repo.get_by_id(gateway_id)
    if not gateway:
        raise HTTPException(status_code=404, detail="Gateway not found")

    return gateway


@gateway_router.get("/imei/{imei}", response_model=GatewayResponse)
def get_gateway_by_imei(imei: str):
    gateway = repo.get_by_imei(imei)
    if not gateway:
        raise HTTPException(status_code=404, detail="Gateway not found")

    return gateway