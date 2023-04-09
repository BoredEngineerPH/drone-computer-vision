from drone.ryze_tello import Drone
import time

drone = Drone()
drone.connect()
# drone.speed(100)
drone.take_off()
drone.show_status()
# time.sleep(5)
# drone.rotate('cw', 360)
# drone.land()
