"""Tello drone object library
"""

# coding=utf-8

from djitellopy_reduced import Tello
import time


class Drone(object):

    def __init__(self):
        self.drone = Tello()
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.send_rc_control = False
        self.drone.connect()
        self.drone.set_speed(10)  # Preset speed
        self.drone.streamoff()
        self.is_flying = False

    def hello(self):
        """Return drone object
        """
        return self.drone

    def kill(self):
        """Kill all motors, be careful in using this command
        as it can damage your drone or hurt someone
        this is only useful if you want to avoid accidental hitting other
        person
        """
        self.drone.emergency()

    def bye(self):
        """Gracefully terminate drone object
        """
        if self.drone.is_flying is True:
            self.drone.end()

    def restart(self):
        """Restart drone, you may need to reconnect to the AP
        """
        self.drone.reboot()

    def speed(self, speed: int):
        """Set speed to speed cm/s.
        Arguments:
            speed: 10-100
        """
        self.drone.set_speed(speed)

    def take_off(self, height: int):
        """Take off to a certain height
        Arguments:
            height: 20-500
        """
        if self.drone.is_flying is not True:
            self.drone.takeoff()
            time.sleep(2)  # Let's put delay before we start climbing. Default 2 seconds
            self.drone.move_up(height)

    def land(self):
        """Land the aircraft
        """
        if self.drone.is_flying is True:
            self.drone.land()

    def up(self, y: int):
        """Ascend to a certain height
        Arguments:
            y: 20-500
        """
        if self.drone.is_flying is True:
            self.drone.move_up(y)

    def down(self, y: int):
        """Descend to a certain height
        Arguments:
            y: 20-500
        """
        if self.drone.is_flying is True:
            self.drone.move_down(y)

    def left(self, x: int):
        """Move left
        Arguments:
            x: 20-500
        """
        if self.drone.is_flying is True:
            self.drone.move_left(x)

    def right(self, x: int):
        """Move right
        Arguments:
            x: 20-500
        """
        if self.drone.is_flying is True:
            self.drone.move_right(x)

    def rotate(self, direction: str, x: int):
        """Rotate x degree
        Arguments:
            direction: cw-ccw
            x: 1-360
        """
        if self.drone.is_flying is True:
            if direction == 'cw':
                self.drone.rotate_clockwise(x)
            if direction == 'ccw':
                self.drone.rotate_counter_clockwise(x)

    def video_off(self):
        """Turn-ff drone camera
        """
        self.drone.streamoff()

    def video_on(self):
        """Turn-on drone camera and set to video mode
        """
        self.drone.streamon()

    def video_stream_data(self):
        """Return video stream data
        """
        return self.drone.get_frame_read()

    def is_video_stream_stopped(self):
        """Check if video stream data is stopped
        """
        return self.drone.get_frame_read().stopped

    def is_flying(self):
        """Check if the drone is flying
        """
        return self.drone.is_flying


    def get_battery(self):
        """Return battery percentage
        """
        return self.drone.get_battery()

    def get_altitude(self):
        """Get current altitude
        """
        return self.drone.get_barometer()

    def get_flight_time(self):
        """Get how long the drone is flying
        """
        return self.drone.get_flight_time()

    def get_temperature(self):
        """Get drone temperature
        """
        return self.drone.get_temperature()