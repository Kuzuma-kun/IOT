print("Xin chào ThingsBoard")
import paho.mqtt.client as mqttclient
import time
import json
from geopy.geocoders import Nominatim
import geocoder

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "NM4ZJdbSG37xO0lnkCBP"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setValue":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

temp = 30
humi = 50
light_intesity = 100
counter = 0

longitude = 106.7
latitude = 10.6

app = Nominatim(user_agent="me")
address = 'Ho Chi Minh City University of Technology'

location = app.geocode(address)
# type(location) -> geopy.location.Location

dictLocation = location.raw  # this is a dict
print(dictLocation)
for i in dictLocation:
    print("%s: %s" % (i, str(dictLocation[i])))

# dict -> json:
jsonLocation = json.dumps(location.raw)  # and this is a Json
print(jsonLocation)
# day la 1 chuoi json, va chuoi json nay ko the truy cap duoc!. De truy cap,
# buoc phai dung json.loads() de bien json thanh dict.


# xem link sau de xem kieu du lieu cua class geopy.location.Location
# https: // geopy.readthedocs.io / en / stable /  #:~:text=Data-,class,geopy.location.Location(address%2C%20point%2C%20raw),-Contains%20a%20parsed
longitude = location.longitude
latitude = location.latitude

while True:
    collect_data = {'temperature': temp, 'humidity': humi, 'light': light_intesity,
                    'longitude': longitude, 'latitude': latitude}  # thang nay la dict

    temp = (temp + 1) % 100
    humi = (humi + 1) % 100
    light_intesity += 1
    client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    time.sleep(5)
