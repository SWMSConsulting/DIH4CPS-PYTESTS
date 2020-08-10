"""
MQTTConnection: This class 

Requirements:
- paho (mqtt api): pip install paho-mqtt (see https://pypi.org/project/paho-mqtt/)

@authors:   Arno Schiller (AS)
@email:     schiller@swms.de
@version:   v0.0.1
@license:   ...

VERSION HISTORY
Version:    (Author) Description:                                           Date:
v0.0.1      (AS) First initialize. ...                                      07.08.2020\n
    
Attributes:
-----------
mqtt_host : str
    the hostname or IP address of the remote broker
user_name : str
    username of the MQTT client
password : str
    password of the MQTT client
port : int
    the network port of the server host to connect to. Defaults to 1883. 
    Note that the default port for MQTT over SSL/TLS is 8883 so if you are 
    using tls_set() or tls_set_context(), the port may need providing manually
keepalive : int
    maximum period in seconds allowed between communications with the broker. 
    If no other messages are being exchanged, this controls the rate at which 
    the client will send ping messages to the broker

local_mqtt : bool
    True    - connect to local MQTT
    False   - connect to mqtt_host

info_list : dict
    list of possible informations to send to MQTT server 
    (API for WebcamRecorder and CloudConnection).
warning_list : dict
    list of possible warnings to send to MQTT server 
    (API for WebcamRecorder and CloudConnection).
error_list : dict
    list of possible errors to send to MQTT server 
    (API for WebcamRecorder and CloudConnection).
"""

import paho.mqtt.client as mqtt
import datetime, time
class MQTTConnection:
    # SSL/TLS1.2 aktivieren. Pub auf den Topic IOT/{irgendwas}
    mqtt_host = "demo2.iotstack.co"
    user_name = "pubclient"
    password = "tiguitto"

    port = 8883
    keepalive = 60

    local_mqtt = True

    info_list = {
        "WebcamRecorder" : {"a" : "b"},
        "CloudConnection" : {
            "FileUploaded": "modul=CloudConnection,process=UploadFile status=0"
        }
    }
    warning_list = {}

    error_list = {
        "WebcamRecorder" : {"a" : "b"},
        "CloudConnection" : {
            # Upload files 
            "FileNotFound": "modul=CloudConnection,process=UploadFile status=8",
            "NoCredentials": "modul=CloudConnection,process=UploadFile status=9",
            "UploadError": "modul=CloudConnection,process=UploadFile status=10"
        }
    
    def __init__(self):
        """ Setup the MQTT connection. 
        """
        self.client = mqtt.Client()
        self.client._username = self.user_name
        self.client._password = self.password
        self.client.on_connect = on_connect
        self.client.on_message = on_message
    
        if self.local_mqtt:
            self.client.connect("localhost", 1883, 60)
        else:
            self.client.connect(self.mqtt_host, self.port, self.keepalive)
        self.client.tls_set()
        self.client.loop_start()

    def testloop(self):
        while True:
            msg = "{0}: test".format(datetime.datetime.now())
            print(msg)
            res = self.client.publish("IOT/test", msg)
            print(res)
            time.sleep(5)
        #print(res)
        #self.client.loop_forever()

    def getInfluxMessage(self, user, message):
        msg = "process,user={0}{1}".format(user, message)
        print(msg)
        # "process,device=windows,processname=WebcamRecorder status=56"
        # measurement(,tag_set) field_set(,field_set) (timestamp)

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server.
    see getting started (https://pypi.org/project/paho-mqtt/)
    """
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("IOT/#")

def on_message(client, userdata, msg):
    """ The callback for when a PUBLISH message is received from the server.
    see getting started (https://pypi.org/project/paho-mqtt/)
    """
    print(msg.topic+" "+str(msg.payload))

if __name__ == '__main__':
    conn = MQTTConnection()
    time.sleep(2)
    #conn.testloop()
    conn.getInfluxMessage("test1", conn.info_list["CloudConnection"]["FileUploaded"])