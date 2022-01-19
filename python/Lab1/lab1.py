print("Xin chào ThingsBoard")
import paho.mqtt.client as mqttclient
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BROKER_ADDRESS = "demo.thingsboard.io"
'''
dia chi host trang web. co the lay source code cua 
thingboard roi tai len server tu tao, luc do 
minh se xai dia chi khac
'''
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "NM4ZJdbSG37xO0lnkCBP"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")

# mqtt giong nhu 1 kenh youtube vay, muon nhan thong bao video moi thi phai
# subcribe vao no, de khi co video moi thi no se ba'o ve` lien
# (qua recv_message)

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
# access token = username de dang nhap vao device.

client.on_connect = connected
# on_connect la 1 ham callback, khi ket 
# noi thanh cong thi no se chui vao ham
# connect (on_connect)
client.connect(BROKER_ADDRESS, 1883) #thuc hien ket noi.
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

temp = 30
humi = 50
light_intensity = 100
counter = 0


# ----------------------------------dia ly------------------------------------------
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.get('https://www.google.com')
# dong code duoi day dung de tao them 1 p co id = "location" chen vao trang web
# thuc te thi cac ham o day deu la ham async, nen ta khong the tra ve 1 gia tri nao ca
# kieu, khi goi ham async, thay vi cho async lam xong thi code di toi dong tiep theo luon
# con ham async chay trong background, khi nao no xong thi no goi ham callback
string = '''
   function getLocation(callback) {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var myjson = {"latitude":position.coords.latitude, "longitude":position.coords.longitude};
                console.log(position);
                console.log(position.coords.latitude);
                console.log(position.coords.longitude); 
                var stringJson = JSON.stringify(myjson);
                callback(stringJson);
            });
        } else {
            console.log("Geolocation is not supported by this browser.");
        }
    }

    getLocation(function(callback) {
        const para = document.createElement("p");
        para.innerHTML = callback;
        para.id = "location";
        document.body.appendChild(para);
    });'''.replace('\n', '').replace('\t', '')

# repeat this code
driver.execute_script(string)
time.sleep(2)
res = driver.find_element(By.ID, "location")
loc = res.text
locDict = json.loads(loc)
longitude = locDict["longitude"]
latitude = locDict["latitude"]
print("latitude: %f, longitude: %f" % (locDict["latitude"], locDict["longitude"]))


# ------------------------------------main code--------------------------------------------------------
while True:
    collect_data = {'temperature': temp, 'humidity': humi, 'light': light_intensity,
                    'longitude': longitude, 'latitude': latitude}  # thang nay la dict
    driver.execute_script(string)
    time.sleep(2)
    res = driver.find_element(By.ID, "location")
    loc = res.text
    locDict = json.loads(loc)
    longitude = locDict["longitude"]
    latitude = locDict["latitude"]
    print("latitude: %f, longitude: %f" % (locDict["latitude"], locDict["longitude"]))
    temp = (temp + 1) % 100
    humi = (humi + 1) % 100
    light_intensity += 1
    client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    time.sleep(8)
