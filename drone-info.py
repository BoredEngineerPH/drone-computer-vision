from lib.drone.ryze_tello import Drone
import sys

# Get drone information
drone = Drone()
drone.hello()
drone.info()
drone.bye()
sys.exit()
