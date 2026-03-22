from pydantic import Json

from src.models.entities import DeviceInfo, Readings
from src.mqtt.frame_utils import MQTTFormattedDataModel, parse_mqtt_frame
from src.repository.db_repository import DeviceInforRepo, GatewayRepo, ReadingsRepo
from src.repository.raw_mqtt_event_repository import RawMqttEventRepository




class MqttService:
    def __init__(self, raw_mqtt_event_repository: RawMqttEventRepository, gateway_repo: GatewayRepo):
        self.raw_mqtt_event_repository = raw_mqtt_event_repository
        self.gateway_repo = gateway_repo
        self.device_infor_repo = DeviceInforRepo()
        self.reading_repo = ReadingsRepo()


    def save_mqtt_raw_frame(self, topic, flat_paload) -> str:
        payload_values = flat_paload.split("/")
        gateway_imei = payload_values[5]

        print('Gateway Id is ',gateway_imei)

        gateway = self.gateway_repo.get_by_imei(gateway_imei)
        print("Gateway is ", gateway.id)

        entity = self.raw_mqtt_event_repository.save(gateway.id, topic, flat_paload)
        print('raw mqtt response is saved ',entity.id)

    def process_mqtt_data_in_reading_data(self, flat_payload) : 
        data :MQTTFormattedDataModel = parse_mqtt_frame(flat_payload)
        print(data)
        device_info: DeviceInfo = self.device_infor_repo.get_by_imei_and_label(data.imei, data.label)
        print('Device info is ', device_info)
        if not device_info:
            print('Invalid IMEI number or davice label')
            return
        json_data = {
            metric: {"value": reading.value, "unit": reading.unit}
            for metric, reading in data.readings.items()
        }

        # 4. Save as a single row
        reading_entry = Readings(
            device_id=device_info.id,
            data=json_data,  # This stores both value and unit
            timestamp=data.timestamp,
            quality_flag=data.flag
        )

        self.reading_repo.save(reading_entry)

