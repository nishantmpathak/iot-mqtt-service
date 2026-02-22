Useful commands

poetry add fastapi uvicorn
poetry add sqlalchemy psycopg2-binary python-dotenv
poetry env activate
poetry run uvicorn src.main:app --reload

http://localhost:8000/docs

To start Docker
docker compose up -d


Install using Homebrew:
brew install mosquitto

Start MQTT Broker
mosquitto

By default it runs on: localhost:1883

🟢 Terminal 1 → Subscribe (Read MQTT Frame)
mosquitto_sub -h localhost -t test/topic -v

This means:

-h localhost → broker address

-t test/topic → topic name

-v → show topic + message

Now it’s waiting to receive messages.



🔵 Terminal 2 → Publish Message
mosquitto_pub -h localhost -t test/topic -m "Hello Nishant"
mosquitto_pub -h localhost -t sensor/data -m '{"deviceId":"D1","temp":31}'


To start Application:
poetry run uvicorn src.main:app --reload


Work done:
Save Gateway
MQTT feame storage


With this MQTT I am able to save frame in DB
mosquitto_pub -h localhost -t sensor/data -m '$/210226/141530/Manufacturing_Section/TataMotor_Bhosri/123123213123213213123/28/3/1/Y/1/231.4,230.8,229.9,13.2,12.7,13.0,9150,0.97,50.01/#'