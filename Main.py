# import json
# import time
# import serial.tools.list_ports
# import paho.mqtt.client as mqttclient
# print("Xin chào ThingsBoard")

# BROKER_ADDRESS = "demo.thingsboard.io"
# PORT = 1883
# THINGS_BOARD_ACCESS_TOKEN = "ep8Xsr7iS12D3E4EQwPj"

# longitude = 106.6297
# latitude = 10.8231


# def subscribed(client, userdata, mid, granted_qos):
#     print("Subscribed...")


# def recv_message(client, userdata, message):
#     print("Received: ", message.payload.decode("utf-8"))
#     temp_data = {'value': True}
#     cmd = 1

#     try:
#         if jsonobj['method'] == "setLED":
#             temp_data['valueLED'] = jsonobj['params']
#             client.publish('v1/devices/me/attributes',
#                            json.dumps(temp_data), 1)

#         elif jsonobj['method'] == "setPUMP":
#             temp_data['valuePUMP'] = jsonobj['params']
#             client.publish('v1/devices/me/attributes',
#                            json.dumps(temp_data), 1)

#     except:
#         pass

#     if len(bbc_port) > 0:
#         ser.write((str(cmd) + "#").encode())


# def connected(client, usedata, flags, rc):
#     if rc == 0:
#         print("Thingsboard connected successfully!!")
#         client.subscribe("v1/devices/me/rpc/request/+")
#     else:
#         print("Connection is failed")


# client = mqttclient.Client("Gateway_Thingsboard")
# client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

# client.on_connect = connected
# client.connect(BROKER_ADDRESS, 1883)
# client.loop_start()

# client.on_subscribe = subscribed
# client.on_message = recv_message


# def getPort():
#     ports = serial.tools.list_ports.comports()
#     N = len(ports)
#     commPort = ""
#     for i in range(0, N):
#         port = ports[i]
#         strPort = str(port)
#         if "USB Serial Device" in strPort:
#             splitPort = strPort.split(" ")
#             commPort = (splitPort[0])
#     return commPort


# mess = ""

# bbc_port = "COM4"
# bbc_port = getPort()
# if len(bbc_port) > 0:
#     print("hello")
#     ser = serial.Serial(port=bbc_port, baudrate=115200)


# def processData(data):
#     data = data.replace("!", "")
#     data = data.replace("#", "")
#     splitData = data.split(":")
#     print(splitData)


# def readSerial():
#     bytesToRead = ser.inWaiting()
#     if (bytesToRead > 0):
#         global mess
#         mess = mess + ser.read(bytesToRead).decode("UTF-8")
#         while ("#" in mess) and ("!" in mess):
#             start = mess.find("!")
#             end = mess.find("#")
#             processData(mess[start:end + 1])
#             if (end == len(mess)):
#                 mess = ""
#             else:
#                 mess = mess[end+1:]


# temp = 30
# humi = 50
# light_intesity = 100
# counter = 0
# while True:
#     if len(bbc_port) > 0:
#         readSerial()
#     time.sleep(1)


import serial.tools.list_ports
import json
import time
import paho.mqtt.client as mqttclient
print("IoT Gateway")

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
mess = ""

# TODO: Add your token and your comport
# Please check the comport in the device manager
THINGS_BOARD_ACCESS_TOKEN = "ep8Xsr7iS12D3E4EQwPj"
bbc_port = "COM4"
if len(bbc_port) > 0:
    ser = serial.Serial(port=bbc_port, baudrate=115200)


def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    # TODO: Add your source code to publish data to the server
    if splitData[1] == "LIGHT":
        light = splitData[2]
        lightStatus = {"light": light}
        client.publish('v1/devices/me/telemetry', json.dumps(lightStatus), 1)
    if splitData[1] == "TEMP":
        temp = splitData[2]
        tempStatus = {"temperature": temp}
        client.publish('v1/devices/me/telemetry', json.dumps(tempStatus), 1)


def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    cmd = 1
    # print(userdata)
    # TODO: Update the cmd to control 2 devices
    try:
        jsonobj = json.loads(message.payload)
        # print(jsonobj)
        if jsonobj['method'] == "setLed":
            temp_data = {'valueLed': True}
            temp_data['valueLed'] = jsonobj['params']
            client.publish('v1/devices/me/attributes',
                           json.dumps(temp_data), 1)
            if (jsonobj['params']):
                cmd = "led-on"
            else:
                cmd = "led-off"
        if jsonobj['method'] == "setFan":
            temp_data = {'valueFan': True}
            temp_data['valueFan'] = jsonobj['params']
            client.publish('v1/devices/me/attributes',
                           json.dumps(temp_data), 1)
            if (jsonobj['params']):
                cmd = "fan-on"
            else:
                cmd = "fan-off"
    except:
        pass
    if len(bbc_port) > 0:
        ser.write((str(cmd) + "#").encode())


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


while True:

    if len(bbc_port) > 0:
        readSerial()

    time.sleep(1)
