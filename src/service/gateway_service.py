from typing import List

from src.models.response.responses import (
    DeviceReadingResponse,
    GatewayReadingsResponse,
    MetricReadingResponse,
    ReadingPayloadResponse,
)
from src.repository.db_repository import GatewayRepo

class GatewayService:
    def __init__(self):
        self.repo = GatewayRepo()

    def get_readings_from_gateway_ids(self, gateway_ids: List[int]) -> List[GatewayReadingsResponse]:
        gateways = self.repo.get_gateways_with_latest_device_readings(gateway_ids)

        grouped_gateways: dict[int, GatewayReadingsResponse] = {}

        for row in gateways:
            gateway_id = row["gateway_id"]

            if gateway_id not in grouped_gateways:
                grouped_gateways[gateway_id] = GatewayReadingsResponse(
                    gateway_id=row["gateway_id"],
                    imei=row["imei"],
                    location=row["gateway_location"],
                    devices=[]
                )

            latest_reading = None
            if row["reading_id"] is not None:
                reading_data = row["reading_data"] or {}

                readings_list = []
                for metric_name, metric_obj in reading_data.items():
                    readings_list.append(
                        MetricReadingResponse(
                            metric=metric_name,
                            metric_value=metric_obj.get("value"),
                            metric_unit=metric_obj.get("unit")
                        )
                    )

                latest_reading = ReadingPayloadResponse(
                    id=row["reading_id"],
                    device_id=row["device_id"],
                    readings=readings_list,
                    timestamp=row["reading_timestamp"],
                    created_at=row["reading_created_at"],
                    quality_flag=row["quality_flag"]
                )

            grouped_gateways[gateway_id].devices.append(
                DeviceReadingResponse(
                    device_id=row["device_id"],
                    label=row["device_label"],
                    location=row["device_location"],
                    device_type=row["device_type"],
                    is_active=row["is_active"],
                    latest_reading=latest_reading
                )
            )

        return list(grouped_gateways.values())