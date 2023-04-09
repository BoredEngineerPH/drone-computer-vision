"""Tello drone object library
"""

# coding=utf-8

from djitellopy_reduced import Tello
import time
import logging


class Drone(object):

    DRONE_SPEED = 10
    MIN_TAKE_OFF_HEIGHT = 70
    LOW_BATT_THRESHOLD = 5
    HIGH_TEMP_THRESHOLD = 30.0
    LOW_TEMP_THRESHOLD = 5.0

    HANDLER = logging.StreamHandler()
    FORMATTER = logging.Formatter('[%(levelname)s] %(filename)s - %(lineno)d - %(message)s')
    HANDLER.setFormatter(FORMATTER)
    LOGGER = logging.getLogger('ryze_tello')
    LOGGER.addHandler(HANDLER)

    def __init__(self, logging_level=None):
        if logging_level is None:
            self.LOGGER.setLevel(logging.INFO)
        else:
            self.LOGGER.setLevel(logging_level)

        self.is_connected = False
        self.drone = Tello()

    def connect(self):
        """Initiate connection to drone
        """
        self.drone.connect()  # Attempt connection or die crashing
        if self.drone.get_battery() > int(self.LOW_BATT_THRESHOLD):
            self.drone.set_speed(self.DRONE_SPEED)
            self.drone.streamoff()
            self.is_connected = True
            self.LOGGER.info('Drone connected..')
        else:
            # Battery too low
            self.LOGGER.warning('Battery too low..')

    def hello(self):
        """Return drone object
        """
        if self.is_connected is True:
            return self.drone
        else:
            self.LOGGER.info('You are not connected to the drone..')

    def can_we_fly(self):
        if self.is_connected is not True:
            self.LOGGER.info('You are not connected to the drone..')
            return False
        elif self.drone.get_battery() <= int(self.LOW_BATT_THRESHOLD):
            self.LOGGER.info('Battery too low..')
            return False
        elif self.drone.get_temperature() < float(self.HIGH_TEMP_THRESHOLD):
            self.LOGGER.info('Too hot to fly, please wait for a couple minutes..')
            return False
        elif self.drone.get_temperature() < float(self.LOW_TEMP_THRESHOLD):
            self.LOGGER.info('Too cold to fly, please wait for a couple minutes..')
            return False
        else:
            return True

    def show_status(self):
        self.LOGGER.info('Battery: ' + str(self.drone.get_battery()))
        self.LOGGER.info('Altitude: ' + str(self.drone.get_barometer()))
        self.LOGGER.info('Average Temp: ' + str(self.drone.get_temperature()))
        self.LOGGER.info('Highest Temp: ' + str(self.drone.get_highest_temperature()))
        self.LOGGER.info('Lowest Temp: ' + str(self.drone.get_lowest_temperature()))

    def kill(self):
        """Kill all motors, be careful in using this command
        as it can damage your drone or hurt someone
        this is only useful if you want to avoid accidental hitting other
        person
        """
        if self.can_we_fly() is True:
            self.LOGGER.warning('Sending kill all human to drone!')
            self.drone.emergency()

    def bye(self):
        """Gracefully terminate drone object
        """
        if self.can_we_fly() is True:
            if self.drone.is_flying is True:
                self.drone.end()

    def restart(self):
        """Restart drone, you may need to reconnect to the AP
        """
        if self.can_we_fly() is True:
            self.drone.reboot()

    def speed(self, speed: int):
        """Set speed to speed cm/s.
        Arguments:
            speed: 10-100
        """
        if self.can_we_fly() is True:
            self.drone.set_speed(speed)

    def take_off(self, initial_height=None):
        """Take off to a certain height
        Arguments:
            initial_height: 20-500
        """
        if self.can_we_fly() is True:
            if self.drone.is_flying is not True:
                self.drone.takeoff()
                if initial_height is not None:
                    if initial_height > self.MIN_TAKE_OFF_HEIGHT:
                        time.sleep(2)  # Let's put delay before we start climbing. Default 2 seconds
                        self.drone.move_up(initial_height)

    def land(self, delay=None):
        """Land the aircraft
        Arguments
            delay: 1-10
        """
        if self.can_we_fly() is True:
            if self.drone.is_flying is True:
                if delay is not None:
                    time.sleep(delay)

                self.drone.land()

    def up(self, y: int):
        """Ascend to a certain height
        Arguments:
            y: 20-500
        """
        if self.can_we_fly() is True:
            if self.drone.is_flying is True:
                self.drone.move_up(y)

    def down(self, y: int):
        """Descend to a certain height
        Arguments:
            y: 20-500
        """
        if self.can_we_fly() is True:
            if self.drone.is_flying is True:
                self.drone.move_down(y)

    def forward(self, x: int):
        """Move drone forward
        Arguments:
            x: 20-500
        """
        if self.can_we_fly() is True:
            self.drone.move_forward(x)

    def backward(self, x: int):
        """Move drone backward
        Arguments:
            x: 20-500
        """
        if self.can_we_fly() is True:
            self.drone.move_back(x)

    def left(self, x: int):
        """Move left
        Arguments:
            x: 20-500
        """
        if self.can_we_fly() is True:
            if self.drone.is_flying is True:
                self.drone.move_left(x)

    def right(self, x: int):
        """Move right
        Arguments:
            x: 20-500
        """
        if self.can_we_fly() is True:
            if self.drone.is_flying is True:
                self.drone.move_right(x)

    def rotate(self, direction: str, x: int):
        """Rotate x degree
        Arguments:
            direction: cw-ccw
            x: 1-360
        """
        if self.can_we_fly() is True:
            if self.drone.is_flying is True:
                if direction == 'cw':
                    self.drone.rotate_clockwise(x)
                if direction == 'ccw':
                    self.drone.rotate_counter_clockwise(x)

    def video_off(self):
        """Turn-ff drone camera
        """
        if self.can_we_fly() is True:
            self.drone.streamoff()

    def video_on(self):
        """Turn-on drone camera and set to video mode
        """
        if self.can_we_fly() is True:
            self.drone.streamon()

    def video_stream_data(self):
        """Return video stream data
        """
        if self.can_we_fly() is True:
            return self.drone.get_frame_read()

    def is_video_stream_stopped(self):
        """Check if video stream data is stopped
        """
        if self.can_we_fly() is True:
            return self.drone.get_frame_read().stopped

    def is_flying(self):
        """Check if the drone is flying
        """
        if self.can_we_fly() is True:
            return True
        else:
            return False

    def get_battery(self):
        """Return battery percentage
        Returns:
            int: 0-100
        """
        if self.can_we_fly() is True:
            return self.drone.get_battery()

    def get_altitude(self):
        """Get current altitude
        Returns:
            int: barometer measurement in cm
        """
        if self.can_we_fly() is True:
            return self.drone.get_barometer()

    def get_flight_time(self):
        """Get how long the drone is flying
        Returns:
            int: flight time in s
        """
        if self.can_we_fly() is True:
            return self.drone.get_flight_time()

    def get_temperature(self):
        """Get drone temperature
        Returns:
            float: average temperature (°C)
        """
        if self.can_we_fly() is True:
            return self.drone.get_temperature()
