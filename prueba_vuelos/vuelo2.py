import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

URI = 'radio://0/70/2M/E7E7E7E7E5'

# Inicializa los drivers
cflib.crtp.init_drivers()

def simple_takeoff_land():
    print("Conectando al Crazyflie...")
    try:
        with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
            print("Conectado.")
            cf = scf.cf

            thrust = 50000  # Puede ajustar según el limite
            duration = 1.0  # Segundos de vuelo

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

if __name__ == '__main__':
    simple_takeoff_land()
