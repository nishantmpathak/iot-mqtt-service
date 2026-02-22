import paho.mqtt.client as mqtt
import json
import threading

from src.mqtt.mqtt_service import MqttService

class MqttClient:
    def __init__(self, mqtt_service):
        self.mqtt_service = mqtt_service
        self.BROKER = "localhost"
        self.PORT = 1883
        self.TOPIC = "sensor/data"

    def on_connect(self, client, userdata, flags, rc):
        print("MQTT Connected:", rc)
        client.subscribe(self.TOPIC)

    def on_message(self, client, userdata, msg):
        print("\nMessage received:")
        payload = msg.payload.decode()
        print("Raw:", payload)
        self.mqtt_service.process_mqtt_received_message(self.TOPIC, payload)


        # try:
        #     data = json.loads(payload)
        #     print("Parsed:", data)
        # except:
        #     print("Invalid JSON")

    def start_mqtt(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(self.BROKER, self.PORT, 60)
        client.loop_forever()

    def run_mqtt_in_thread(self):
        thread = threading.Thread(target=self.start_mqtt)
        thread.daemon = True
        thread.start()