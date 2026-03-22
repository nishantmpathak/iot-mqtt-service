from src.models.entities import Readings
from src.models.request.gateway_request import DeviceFilterRequest
from src.models.response.responses import DeviceReadingResponse, FullReadingResponse, GetReadingsForDevice, MetricReadingResponse
from src.repository.db_repository import DeviceInforRepo, GatewayRepo, ReadingsRepo


class DeviceService():
    def __init__(self):
        self.reading_repo = ReadingsRepo()
        self.device_repo = DeviceInforRepo()
        self.gateway_repo = GatewayRepo()
        
        pass

    def get_device_readings_filter(self, payload: DeviceFilterRequest) -> list[DeviceReadingResponse]:
        devices:list[DeviceReadingResponse] = []
        for d_id in payload.device_ids:
            device_info = self.device_repo.get_by_id(d_id)
            if not device_info:
                continue
            
            db_readings: list[Readings] = self.reading_repo.get_filtered_readings(
                device_ids=[d_id], start_date=payload.start_date, end_date=payload.end_date, shift=payload.shift_details
            )


            formatted_readings: list[FullReadingResponse] = []
            metric_list = []
            for r in db_readings:
                metric_list: list[MetricReadingResponse] = [
                    {'metric' : k, 'metric_value':v['value'], 'metric_unit': v['unit']}
                    for k, v in r.data.items()
                ]
            
                formatted_readings.append({
                        "id": r.id,
                        "readings": metric_list,
                        "timestamp": r.timestamp,
                        "created_at": r.created_at,
                        "quality_flag": r.quality_flag
                    })
                print('formatted_readings is ', formatted_readings)
            
            devices.append({
                "device_id": device_info.id,
                "label": device_info.label,
                "location": device_info.location,
                "device_type": device_info.device_type,
                "is_active": device_info.is_active,
                "formatted_readings": formatted_readings
            })

        return devices