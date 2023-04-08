from drone.ryze_tello import Drone

drone = Drone()
drone.take_off(200)
drone.rotate('cw', 360)
drone.land()
