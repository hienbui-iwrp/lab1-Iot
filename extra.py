import re
import subprocess as sp
import requests
import json
import time
import paho.mqtt.client as mqttclient

print("Xin chào ThingsBoard")

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "M9iN1Iao30Xng6U5HAW8"

res = requests.get('https://ipinfo.io/')
print(res.text)


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setValue":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes',
                           json.dumps(temp_data), 1)
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

counter = 0
accuracy = 3 

while True:
    pshellcomm = ['powershell']
    pshellcomm.append('add-type -assemblyname system.device; '
                      '$loc = new-object system.device.location.geocoordinatewatcher;'
                      '$loc.start(); '
                      'while(($loc.status -ne "Ready") -and ($loc.permission -ne "Denied")) '
                      '{start-sleep -milliseconds 100}; '
                      '$acc = %d; '
                      'while($loc.position.location.horizontalaccuracy -gt $acc) '
                      '{start-sleep -milliseconds 100; $acc = [math]::Round($acc*1.5)}; '
                      '$loc.position.location.latitude; '
                      '$loc.position.location.longitude; '
                      '$loc.position.location.horizontalaccuracy; '
                      '$loc.stop()' % (accuracy))

    p = sp.Popen(pshellcomm, stdin=sp.PIPE, stdout=sp.PIPE,
                 stderr=sp.STDOUT, text=True)
    (out, err) = p.communicate()
    out = re.split('\n', out)

    latitude = float(out[0])
    longitude = float(out[1])
    radius = int(out[2])

    collect_data = {'longitude': longitude, 'latitude': latitude}
    client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    time.sleep(10)
