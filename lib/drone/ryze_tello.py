"""Tello drone object library

This class standardized the implementation of drone control, there might
be other features the drone may offer.
"""

# coding=utf-8

from djitellopy import Tello
import time
from lib.drone.AbstractDroneBase import AbstractDroneBase


class Drone(AbstractDroneBase):
    DRONE = None
    parent = None
    __VIDEO_STREAM_FRAMES = None

    def hello(self):
        self.parent = super()
        self.parent.setup('ryze_tello')

        # Initialize tello object
        self.DRONE = Tello()

        if self.parent.is_connected is not True:
            self.DRONE.connect()
            self.parent.im_connected(True)  # Set connection flag to True

            # Since we are now connected let's set our telemetry,
            # so we can use can_we_fly() method, we can also call this in realtime
            self.update_telemetry()

    def update_telemetry(self):
        self.parent.set_telemetry('battery', self.DRONE.get_battery())
        self.parent.set_telemetry('altitude', self.DRONE.get_barometer())
        self.parent.set_telemetry('low_temp', self.DRONE.get_lowest_temperature())
        self.parent.set_telemetry('high_temp', self.DRONE.get_highest_temperature())
        self.parent.set_telemetry('average_temp', self.DRONE.get_temperature())

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
        if self.parent.can_we_fly is True:
            self.DRONE.takeoff()
            if altitude is not None:
                self.DRONE.move_up(altitude)

    def land(self, delay=None):
        if self.parent.can_we_land is True:
            if delay is not None:
                time.sleep(delay)
            self.DRONE.land()

    def ascend(self, v: int):
        if self.parent.can_we_fly is True:
            self.DRONE.move_up(v)

    def descend(self, v: int):
        if self.parent.can_we_fly is True:
            self.DRONE.move_down(v)

    def forward(self, v: int):
        if self.parent.can_we_fly is True:
            self.DRONE.move_forward(v)

    def backward(self, v: int):
        if self.parent.can_we_fly is True:
            self.DRONE.move_back(v)

    def left(self, v: int):
        if self.parent.can_we_fly is True:
            self.DRONE.move_left(v)

    def right(self, v: int):
        if self.parent.can_we_fly is True:
            self.DRONE.move_right(v)

    def rotate_left(self, v: int):
        if self.parent.can_we_fly is True:
            self.DRONE.rotate_counter_clockwise(v)

    def rotate_right(self, v: int):
        if self.parent.can_we_fly is True:
            self.DRONE.rotate_clockwise(v)

    def rc_command(self, roll: int, pitch: int, throttle: int, yaw: int):
        self.DRONE.send_rc_control(roll, pitch, throttle, yaw)

    def start_video_streaming(self):
        if self.parent.is_connected is True:
            self.DRONE.streamoff()  # Just incase it was never closed properly
            self.DRONE.streamon()
            # Let's update the flag so any function that requires video frame
            # is aware of
            self.parent.im_video_streaming(True)

    def stop_video_streaming(self):
        if self.parent.is_connected is True:
            self.DRONE.streamoff()
            self.parent.im_video_streaming(False)

    def get_video_frames(self):
        if self.parent.is_connected is True and self.parent.is_video_streaming:
            return self.DRONE.get_frame_read()

    def get_battery(self):
        if self.parent.is_connected is True:
            return self.DRONE.get_battery()

    def get_temperature(self):
        if self.parent.is_connected is True:
            return self.DRONE.get_temperature()

    def get_altitude(self):
        if self.parent.is_connected is True:
            return self.DRONE.get_barometer()