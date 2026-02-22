from src.repository.Gateway_repository import GatewayRepo
from src.repository.raw_mqtt_event_repository import RawMqttEventRepository


class MqttService:
    def __init__(self, raw_mqtt_event_repository: RawMqttEventRepository, gateway_repo: GatewayRepo):
        self.raw_mqtt_event_repository = raw_mqtt_event_repository
        self.gateway_repo = gateway_repo


    def process_mqtt_received_message(self, topic, flat_paload) -> str:
        payload_values = flat_paload.split("/")
        gateway_imei = payload_values[5]

        print('Gateway Id is ',gateway_imei)

        gateway = self.gateway_repo.get_by_imei(gateway_imei)
        print("Gateway is ", gateway.id)

        entity = self.raw_mqtt_event_repository.save(gateway.id, topic, flat_paload)
        print('raw mqtt response is saved ',entity.id)

