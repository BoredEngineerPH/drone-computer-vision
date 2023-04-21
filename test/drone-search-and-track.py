from lib.drone.ryze_tello import Drone
import pygame
import numpy as np
import time
import cv2
import sys
import os

DRONE_SPEED = 60
# Root Dire
ROOTDIR = sys.path[1]


class DroneSearchTrack(object):

    # +--------------------------------------------------------------+
    # PyGame variables
    # +--------------------------------------------------------------+
    # Frames per second of the pygame window display
    # A low number also results in input lag, as input information is processed once per frame.
    DISPLAY_FPS = 120
    DISPLAY_MODE = [960, 720]  # Display window size

    # +--------------------------------------------------------------+
    # Drone object variables
    # +--------------------------------------------------------------+
    DRONE = None  # Drone object instance

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Video Stream")
        self.screen = pygame.display.set_mode(self.DISPLAY_MODE)

        # Instantiate drone object
        self.DRONE = Drone()

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // self.DISPLAY_FPS)

        # Load cascade
        cascade_file = sys.path[1] + "/data/haarcascades/haarcascade_frontalface_default.xml"
        self.object_cascade = cv2.CascadeClassifier(cascade_file)

    def run(self):
        # Initiate connection to drone object
        self.DRONE.hello()
        # Start video streaming
        self.DRONE.start_video_streaming()

        frame_read = self.DRONE.get_video_frames()
        should_stop = False
        while not should_stop:

            if self.DRONE.is_low_battery is True:
                # Gracefully exit
                self.DRONE.bye()

            if frame_read.stopped:
                break

            self.screen.fill([0, 0, 0])

            frame = frame_read.frame

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)

            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()
            time.sleep(1 / self.DISPLAY_FPS)

        # Call it always before finishing. To deallocate resources.
        self.DRONE.bye()

    def keydown(self, key):
        """ Set RC channel variables from key down, we use standard 4-channel control
        Arguments:
            key: pygame key
        """

    def keyup(self, key):
        """ Set RC channel variables from key release, we use standard 4-channel control
        Arguments:
            key: pygame key
        """

    def send_rc_command(self):
        """ Send 4-channel rc command """
        if self.DRONE_SEND_RC_COMMAND is True:
            self.DRONE.rc_command(self.VELOCITY_LEFT_RIGHT,
                                  self.VELOCITY_FORWARD_BACK,
                                  self.VELOCITY_UP_DOWN,
                                  self.VELOCITY_YAW)



drone = DroneSearchTrack()
drone.run()
