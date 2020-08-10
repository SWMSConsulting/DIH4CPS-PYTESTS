"""
SystemMonitoring: This class rules the system monitoring.

Requirements:

@authors:   Arno Schiller (AS)
@email:     schiller@swms.de
@version:   v0.0.1
@license:   ...

VERSION HISTORY
Version:    (Author) Description:                                           Date:
v0.0.1      (AS) First initialize. Added random numbers to test.            10.08.2020\n
"""

from configuration import *
from mqtt_connection import MQTTConnection
import time

class SystemMonitoring:
    """ 
    SystemMonitoring: This class rules the system monitoring. Tracked values:
    -
    -
    
    Attributes:
    -----------
    user_name : str
        name of the current system (e.g. test1)
    module_name : str
        name of this class
    """

    user_name = global_user_name
    module_name = "SystemMonitoring"
    
    def __init__(self):
        self.mqtt = MQTTConnection()


    def uploadSystemMeasurement(self):
        cpu_temperature = 20
        msg = "temperature,location=CPU,modul={0},user={1}".format(self.module_name,
                                                                self.user_name)
        cpu_msg = msg + " temperature={}".format(cpu_temperature)
        print(cpu_msg)
        self.mqtt.sendMessage(cpu_msg)

if __name__ == "__main__":
    monitoring = SystemMonitoring()
    while True:
        monitoring.uploadSystemMeasurement()
        time.sleep(10)
