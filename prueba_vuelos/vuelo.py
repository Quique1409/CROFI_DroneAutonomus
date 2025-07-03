'''Prueba de conexión'''

#Important
import logging
import time
import cflib.crtp
from cflib.crazyflie import Crazyflie #connect 
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger 
from cflib.utils import uri_helper

#URI to the Crazyflie to connect to
uri = uri_helper.uri_from_env(default='radio://0/70/2M/E7E7E7E7E5')

#only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

#Funtion for connecting
def simple_connect():

    print("Connected :)")
    time.sleep(5)
    print("Disconnect :(")

#Funtion main

if __name__ == '__main__':
    #Initialize the low-level drivers
    cflib.crtp.init_drivers()

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        simple_connect()