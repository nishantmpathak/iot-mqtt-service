from typing import Optional

from src.db.database import SessionLocal
from src.models.gateway import DeviceInfo, Gateway


class GatewayRepo:
    def __init__(self):
        self.db = SessionLocal()

    def save(self, imei:str, location:Optional[str]) -> Gateway:
        print("calling save from gateway repo")
        try:
            gateway = Gateway(
                imei = imei, 
                location = location
            )
            self.db.add(gateway)
            self.db.commit()
            self.db.refresh(gateway)
        finally:
            self.db.close()
        return gateway

    def get_by_id(self, gateway_id: int) -> Optional[Gateway]:
        try:
            return self.db.query(Gateway).filter(Gateway.id == gateway_id).first()
        finally:
            self.db.close()

    def get_by_imei(self, imei: str) -> Optional[Gateway]:
        print('calling get_by_imei')
        try:
            return self.db.query(Gateway).filter(Gateway.imei == imei).first()
        finally:
            self.db.close()

    # def get_all(self) -> list[Gateway]:
    #     db = SessionLocal()
    #     try:
    #         return db.query(Gateway).all()
    #     finally:
    #         db.close()

    # def delete(self, gateway_id: int) -> None:
    #     db = SessionLocal()
    #     try:
    #         gateway = db.query(Gateway).filter(Gateway.id == gateway_id).first()
    #         if gateway:
    #             db.delete(gateway)
    #             db.commit()
    #     finally:
    #         db.close()

class DeviceInforRepo:
    def __init__(self):
        self.db = SessionLocal()

    def save(self, device: DeviceInfo) -> DeviceInfo:
        try:
            self.db.add(device)
            self.db.commit()
            self.db.refresh(device)
        finally:
            self.db.close()
        return device
    
    def get_by_id(self, id:str):
        try:
            return self.db.query(DeviceInfo).filter(DeviceInfo.id == id).first()
        finally:
            self.db.close()


