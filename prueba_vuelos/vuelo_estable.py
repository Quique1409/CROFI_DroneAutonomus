import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
import time, threading

'''
    Variables que se pueden cambiar solo thrust, duration, hover
    thrust se puede cambiar en un rango de 0 65535
    hover se puede cambiar en un rango de 0 65535
    duration cambia el tiempo que mantiene vuelo tanto en el takeoff y en el hover
'''

URI = 'radio://0/70/2M/E7E7E7E7E5'

abort_event = threading.Event()

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
            hover_thrust = 48000 #Sustentación de ajuste (levita)
            takeoof_time = 2    # Segundos de vuelo
            hover_time = 2      #Segundos de nivelación

            #launch
            start_time = time.time()
            while time.time() - start_time < takeoof_time:
                cf.commander.send_setpoint(0,0,0, takeoff_thrust)
                time.sleep(0.1)

            #Hover
            start_time =time.time()
            while time.time() - start_time < hover_time:
                cf.commander.send_setpoint(0,0,0, hover_thrust)
                time.sleep(0.1)

            for i in range(hover_thrust, 20000, -1000):
                cf.commander.send_setpoint(0,0,0,i)
                time.sleep(0.1)

            cf.commander.send_setpoint(0,0,0,0)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    '''
    Si se quiere cambiar de funcion (diferente rutina) cambiar la línea de abajo por:
    simple_takeoff_land || solo vuela y aterriza lento
    tekeoff_hover_land || se queda volando a un nivel
    '''
    # Inicializa los drivers
    cflib.crtp.init_drivers()


    try:
        takeoff_hover_land() #Aquí se cambia.

    except KeyboardInterrupt:
        abort_event.set()
        print("\n Aterrizaje de emergencia ACTIVADO")

