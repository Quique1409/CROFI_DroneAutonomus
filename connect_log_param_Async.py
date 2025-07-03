import logging
import time

import cflib.crtp #Scan for Crazyflie instances
from cflib.crazyflie import Crazyflie #Used to easily connect/send/receive data from a CRazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie 
from cflib.utils import uri_helper #It handles the asynchronous nature of the Crazyflie API and turns it into blocking function.

#Step 2a. LOgging (synchronous)
from cflib.crazyflie.log import LogConfig # Enables logging from the Crazyflie
from cflib.crazyflie.syncLogger import SyncLogger #Provides synchronous acces to log data from the Crazyflie


# URI to the Crazyflie to connect to
uri = uri_helper.uri_from_env(default='radio://0/70/2M/E7E7E7E7E5')
#ONly output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

#Logging Asynchronous
def log_stab_callback(timestamp, data, logconf):
    print('[%d][%s]: %s' % (timestamp, logconf.name, data))


def simple_log_async(scf, logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(log_stab_callback)
    logconf.start()
    time.sleep(5)
    logconf.stop()

'''
#Logging Synchronous
def simple_log(scf, logconf):
    with SyncLogger(scf, lg_stab) as logger:
        for log_entry in logger:
            timestamp = log_entry[0]
            data = log_entry[1]
            logconf_name = log_entry[2]
            print('[%d][%s]: %s'%(timestamp, logconf_name, data))

            break
            
def simple_connect():
    print("Yeah, I'm connected! :D")
    time.sleep(3)
    print("Now I will disconnect :'(")
'''

if __name__=='__main__':
    #Initialize the low-level drivers
    cflib.crtp.init_drivers()

    lg_stab = LogConfig(name= 'Stabilizer', period_in_ms=10)
    lg_stab.add_variable('stabilizer.roll', 'float')
    lg_stab.add_variable('stabilizer.pitch', 'float')
    lg_stab.add_variable('stabilizer.yaw', 'float')

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        
        #simple_connect()
        simple_log_async(scf, lg_stab)