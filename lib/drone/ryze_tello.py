"""Tello drone object library

This class standardized the implementation of drone control, there might
be other features the drone may offer.
"""

# coding=utf-8

from djitellopy_reduced import Tello
import time
from lib.drone.AbstractDroneBase import AbstractDroneBase


class Drone(AbstractDroneBase):
    DRONE = None
    parent = None

    def hello(self):
        self.parent = super()
        self.parent.setup('ryze_tello')

        # Initialize tello object
        self.DRONE = Tello()

        if self.parent.is_connected() is not True:
            self.DRONE.connect()
            self.parent.im_connected(True)  # Set connection flag to True

            # Since we are now connected let's set our telemetry, so we can use can_we_fly() method
            self.parent.set_telemetry('battery', self.DRONE.get_battery())
            self.parent.set_telemetry('altitude', self.DRONE.get_barometer())
            self.parent.set_telemetry('low_temp', self.DRONE.get_lowest_temperature())
            self.parent.set_telemetry('high_temp', self.DRONE.get_highest_temperature())
            self.parent.set_telemetry('average_temp', self.DRONE.get_temperature())
            self.parent.set_telemetry('drone_firmware_version', self.DRONE.query_sdk_version())

    def bye(self):
        self.parent.closing()
        self.DRONE.end()

    def instance(self):
        return self.DRONE

    def kill(self):
        self.DRONE.emergency()

    def restart(self):
        self.DRONE.reboot()

    def speed(self, speed: int):
        self.DRONE.set_speed(speed)

    def takeoff(self, altitude=None):
        if self.parent.can_we_fly() is True:
            self.DRONE.takeoff()
            if altitude is not None:
                self.DRONE.move_up(altitude)

    def land(self, delay=None):
        if self.parent.can_we_fly() is True:
            if delay is not None:
                time.sleep(delay)
            self.DRONE.land()

    def ascend(self, v: int):
        if self.parent.can_we_fly() is True:
            self.DRONE.move_up(v)

    def descend(self, v: int):
        if self.parent.can_we_fly() is True:
            self.DRONE.move_down(v)

    def forward(self, v: int):
        if self.parent.can_we_fly() is True:
            self.DRONE.move_forward(v)

    def backward(self, v: int):
        if self.parent.can_we_fly() is True:
            self.DRONE.move_back(v)

    def left(self, v: int):
        if self.parent.can_we_fly() is True:
            self.DRONE.move_left(v)

    def right(self, v: int):
        if self.parent.can_we_fly() is True:
            self.DRONE.move_right(v)

    def rotate_ccw(self, v: int):
        if self.parent.can_we_fly() is True:
            self.DRONE.rotate_counter_clockwise(v)

    def rotate_cw(self, v: int):
        if self.parent.can_we_fly() is True:
            self.DRONE.rotate_clockwise(v)

    def start_video_streaming(self):
        if self.parent.is_connected() is True:
            self.DRONE.streamoff()  # Just incase it was never closed properly
            self.DRONE.streamon()

    def end_video_streaming(self):
        if self.parent.is_connected() is True:
            self.DRONE.streamoff()
