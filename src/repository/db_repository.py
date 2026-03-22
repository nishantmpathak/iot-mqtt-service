from datetime import date
from typing import Optional

from sqlalchemy import Date, Time, and_, cast, func, desc
from sqlalchemy.orm import Query

from src.db.database import SessionLocal
from src.models.entities import DeviceInfo, Gateway, Readings
from src.models.request.gateway_request import ShiftDetails


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

    def get_all_gateways(self) -> list[Gateway]:
        """Fetches all gateway records from the database."""
        try:
            return self.db.query(Gateway).all()
        finally:
            self.db.close()



    def get_gateways_with_latest_device_readings(self, gateway_ids: list[int]) -> list[dict]:
        try:
            latest_reading_subquery = (
                self.db.query(
                    Readings.id.label("reading_id"),
                    Readings.device_id.label("device_id"),
                    Readings.data.label("reading_data"),
                    Readings.timestamp.label("reading_timestamp"),
                    Readings.created_at.label("reading_created_at"),
                    Readings.quality_flag.label("quality_flag"),
                    func.row_number().over(
                        partition_by=Readings.device_id,
                        order_by=(
                            desc(Readings.created_at),
                            desc(Readings.timestamp),
                            desc(Readings.id),
                        )
                    ).label("rn")
                )
                .subquery()
            )

            query = (
                self.db.query(
                    Gateway.id.label("gateway_id"),
                    Gateway.imei.label("imei"),
                    Gateway.location.label("gateway_location"),

                    DeviceInfo.id.label("device_id"),
                    DeviceInfo.label.label("device_label"),
                    DeviceInfo.location.label("device_location"),
                    DeviceInfo.device_type.label("device_type"),
                    DeviceInfo.is_active.label("is_active"),

                    latest_reading_subquery.c.reading_id.label("reading_id"),
                    latest_reading_subquery.c.reading_data.label("reading_data"),
                    latest_reading_subquery.c.reading_timestamp.label("reading_timestamp"),
                    latest_reading_subquery.c.reading_created_at.label("reading_created_at"),
                    latest_reading_subquery.c.quality_flag.label("quality_flag"),
                )
                .join(DeviceInfo, DeviceInfo.gateway_id == Gateway.id)
                .outerjoin(
                    latest_reading_subquery,
                    (latest_reading_subquery.c.device_id == DeviceInfo.id)
                    & (latest_reading_subquery.c.rn == 1)
                )
                .filter(Gateway.id.in_(gateway_ids))
                .order_by(Gateway.id, DeviceInfo.id)
            )

            rows = query.all()

            return [
                {
                    "gateway_id": row.gateway_id,
                    "imei": row.imei,
                    "gateway_location": row.gateway_location,
                    "device_id": row.device_id,
                    "device_label": row.device_label,
                    "device_location": row.device_location,
                    "device_type": row.device_type,
                    "is_active": row.is_active,
                    "reading_id": row.reading_id,
                    "reading_data": row.reading_data,
                    "reading_timestamp": row.reading_timestamp,
                    "reading_created_at": row.reading_created_at,
                    "quality_flag": row.quality_flag,
                }
                for row in rows
            ]
        finally:
            self.db.close()

  
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

    def get_by_imei_and_label(self, imei: str, label: str) -> Optional[DeviceInfo]:
        """
        Joins DeviceInfo with Gateway to find a device based on 
        the Gateway's IMEI and the Device's Label.
        """
        try:
            return (
                self.db.query(DeviceInfo)
                .join(Gateway, DeviceInfo.gateway_id == Gateway.id)
                .filter(Gateway.imei == imei)
                .filter(DeviceInfo.label == label)
                .first()
            )
        finally:
            self.db.close()


class ReadingsRepo:
    def __init__(self):
        # We create the session here, but we must be careful!
        self.db = SessionLocal()

    def get_by_id(self, id: int) -> Readings:
        try:
            reading = self.db.query(Readings).filter(Readings.id == id).first()
            if reading:
                # This 'detaches' the object so it stays valid after db.close()
                self.db.expunge(reading) 
            return reading
        finally:
            self.db.close()

    def save(self, reading: Readings) -> Readings:
        try:
            self.db.add(reading)
            self.db.commit()
            self.db.refresh(reading)
            return reading
        finally:
            self.db.close()
            
    
    def get_filtered_readings(self, device_ids: list[int], start_date: date, end_date: date, shift: Optional[ShiftDetails] = None) -> list[Readings]:
        try:
            query: Query[Readings] = self.db.query(Readings).filter(
                Readings.device_id.in_(device_ids),
                cast(expression=Readings.timestamp, type_=Date) >= start_date,
                cast(expression=Readings.timestamp, type_=Date) <= end_date
            )

            if shift:
                # Handle shift logic (handles both normal shifts and overnight shifts)
                s_time = shift.start_time
                e_time = shift.end_time
                
                if s_time <= e_time:
                    query = query.filter(
                        cast(expression=Readings.timestamp, type_=Time) >= s_time,
                        cast(expression=Readings.timestamp, type_=Time) <= e_time
                    )
                else: # Overnight shift (e.g., 22:00 to 06:00)
                    query = query.filter(
                        (cast(expression=Readings.timestamp, type_=Time) >= s_time) | 
                        (cast(expression=Readings.timestamp, type_=Time) <= e_time)
                    )

            return query.order_by(Readings.timestamp.asc()).all()
        finally:
            self.db.close()
        
