import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

'''
    Variables que se pueden cambiar solo thrust y duration
    thrust se puede cambiar en un rango de 0 65535
    duration cambia el tiempo que mantiene vuelo 
'''

URI = 'radio://0/70/2M/E7E7E7E7E5'

# Inicializa los drivers
cflib.crtp.init_drivers()

def simple_takeoff_land():
    print("Conectando al Crazyflie...")
    try:
        with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
            print("Conectado.")
            cf = scf.cf

            thrust = 50000  # Puede ajustar según el limite || de 0 a 65535
            duration = 2  # Segundos de vuelo

            print("Despegando...")
            start_time = time.time()
            while time.time() - start_time < duration:
                cf.commander.send_setpoint(0, 0, 0, thrust)
                time.sleep(0.1)

            print("Aterrizando...")
            for t in range(thrust, 20000, -1000):
                cf.commander.send_setpoint(0, 0, 0, t)
                time.sleep(0.1)

            # Apagar motores
            cf.commander.send_setpoint(0, 0, 0, 0)
            print("Vuelo completado.")

    except Exception as e:
        print(f"Error: {e}")

#Funtion hover 
def takeoff_hover_land():
    try:
        with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
            cf = scf.cf

            takeoff_thrust = 50000 # Puede ajustar según el limite || de 0 a 65535
            hover_thrust = 38000 #Sustentación de ajuste (levita)
            takeoof_time = 2    # Segundos de vuelo
            hover_time = 5

            #launch
            t0= time.time()
            while time.time() - t0 < takeoof_time:
                cf.commander.send_setpoint(0,0,0, takeoff_thrust)
                time.sleep(0.1)

            #Hover
            t0=time.time()
            while time.time() - t0 < hover_time:
                cf.commander.send_setpoint(0,0,0, hover_thrust)
                time.sleep(0.1)

            for i in range(hover_thrust, 18000, -1000):
                cf.commander.send_setpoint(0,0,0,i)
                time.sleep(0.1)

            cf.commander.send_setpoint(0,0,0,0)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    takeoff_hover_land()
