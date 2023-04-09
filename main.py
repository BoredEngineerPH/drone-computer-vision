from drone.ryze_tello import Drone

drone = Drone()
drone.take_off()
drone.rotate('cw', 360)
drone.land()
