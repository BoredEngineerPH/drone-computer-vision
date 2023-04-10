from lib.drone.ryze_tello import Drone
import pygame
import numpy as np
import time
import cv2
import sys

DRONE_SPEED = 60


class DroneController(object):
    # +--------------------------------------------------------------+
    # Keymaps
    # +--------------------------------------------------------------+
    KEY_QUIT = pygame.K_q
    KEY_TAKEOFF = pygame.K_t
    KEY_LANDING = pygame.K_l

    # Mode 1
    MODE1_KEY_THROTTLE_UP = pygame.K_UP  # Ascend
    MODE1_KEY_THROTTLE_DOWN = pygame.K_DOWN  # Descend
    MODE1_KEY_ROLL_LEFT = pygame.K_LEFT  # Move Left
    MODE1_KEY_ROLL_RIGHT = pygame.K_RIGHT  # Move Right
    MODE1_KEY_PITCH_UP = pygame.K_s  # Move backward
    MODE1_KEY_PITCH_DOWN = pygame.K_w  # Move forward
    MODE1_KEY_YAW_LEFT = pygame.K_a  # Rotate ccw
    MODE1_KEY_YAW_RIGHT = pygame.K_d  # Rotate cw

    # Mode 2
    MODE2_KEY_THROTTLE_UP = pygame.K_w  # Ascend
    MODE2_KEY_THROTTLE_DOWN = pygame.K_s  # Descend
    MODE2_KEY_ROLL_LEFT = pygame.K_LEFT  # Move Left
    MODE2_KEY_ROLL_RIGHT = pygame.K_RIGHT  # Move Right
    MODE2_KEY_PITCH_UP = pygame.K_UP  # Move backward
    MODE2_KEY_PITCH_DOWN = pygame.K_DOWN  # Move forward
    MODE2_KEY_YAW_LEFT = pygame.K_a  # Rotate ccw
    MODE2_KEY_YAW_RIGHT = pygame.K_d  # Rotate cw

    # Mode 3
    MODE3_KEY_THROTTLE_UP = pygame.K_UP  # Ascend
    MODE3_KEY_THROTTLE_DOWN = pygame.K_DOWN  # Descend
    MODE3_KEY_ROLL_LEFT = pygame.K_a  # Move Left
    MODE3_KEY_ROLL_RIGHT = pygame.K_d  # Move Right
    MODE3_KEY_PITCH_UP = pygame.K_w  # Move backward
    MODE3_KEY_PITCH_DOWN = pygame.K_s  # Move forward
    MODE3_KEY_YAW_LEFT = pygame.K_LEFT  # Rotate ccw
    MODE3_KEY_YAW_RIGHT = pygame.K_RIGHT  # Rotate cw

    # Mode 4
    MODE4_KEY_THROTTLE_UP = pygame.K_w  # Ascend
    MODE4_KEY_THROTTLE_DOWN = pygame.K_s  # Descend
    MODE4_KEY_ROLL_LEFT = pygame.K_a  # Move Left
    MODE4_KEY_ROLL_RIGHT = pygame.K_d  # Move Right
    MODE4_KEY_PITCH_UP = pygame.K_UP  # Move backward
    MODE4_KEY_PITCH_DOWN = pygame.K_DOWN  # Move forward
    MODE4_KEY_YAW_LEFT = pygame.K_LEFT  # Rotate ccw
    MODE4_KEY_YAW_RIGHT = pygame.K_RIGHT  # Rotate cw

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
    DRONE_SEND_RC_COMMAND = False

    # Drone velocities between -100~100
    VELOCITY_FORWARD_BACK = 0
    VELOCITY_LEFT_RIGHT = 0
    VELOCITY_UP_DOWN = 0
    VELOCITY_YAW = 0

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Video Stream")
        if self.DISPLAY_MODE == 'fullscreen':
            self.screen = pygame.display.set_mode([0, 0],
                                                  pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.DISPLAY_MODE)

        # Instantiate drone object
        self.DRONE = Drone()

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // self.DISPLAY_FPS)

        # Set keymap, update what suits your need, standard default
        # on most drone is mode 2
        self.KEY_UP, self.KEY_DOWN, \
            self.KEY_LEFT, self.KEY_RIGHT, \
            self.KEY_BACKWARD, self.KEY_FORWARD, \
            self.KEY_ROTATE_LEFT, self.KEY_ROTATE_RIGHT = (self.MODE2_KEY_THROTTLE_UP, self.MODE2_KEY_THROTTLE_DOWN,
                                                           self.MODE2_KEY_ROLL_LEFT, self.MODE2_KEY_ROLL_RIGHT,
                                                           self.MODE2_KEY_PITCH_DOWN, self.MODE2_KEY_PITCH_UP,
                                                           self.MODE2_KEY_YAW_LEFT, self.MODE2_KEY_YAW_RIGHT)

    def run(self):

        # Initiate connection to drone object
        self.DRONE.hello()
        # Start video streaming
        self.DRONE.start_video_streaming()

        frame_read = self.DRONE.get_video_frames()
        should_stop = False
        while not should_stop:

            if self.DRONE.is_low_battery is True:
                # Gracefull exit
                self.DRONE.bye()
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.send_rc_command()
                elif event.type == pygame.QUIT:
                    self.DRONE.bye()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == self.KEY_QUIT:
                        should_stop = True
                    else:
                        self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup(event.key)

            if frame_read.stopped:
                break

            self.screen.fill([0, 0, 0])

            frame = frame_read.frame

            # Add drone stats to display
            text = "Bat: {battery}%, Temp: {temp}°C, Alt: {alt}cm".format(battery=self.DRONE.get_battery(),
                                                                          temp=self.DRONE.get_temperature(),
                                                                          alt=self.DRONE.get_altitude())
            cv2.putText(frame, text, (5, 720 - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

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
        if key == self.KEY_FORWARD:
            self.VELOCITY_FORWARD_BACK = DRONE_SPEED
        elif key == self.KEY_BACKWARD:
            self.VELOCITY_FORWARD_BACK = -DRONE_SPEED
        elif key == self.KEY_LEFT:
            self.VELOCITY_LEFT_RIGHT = -DRONE_SPEED
        elif key == self.KEY_RIGHT:
            self.VELOCITY_LEFT_RIGHT = DRONE_SPEED
        elif key == self.KEY_UP:
            self.VELOCITY_UP_DOWN = DRONE_SPEED
        elif key == self.KEY_DOWN:
            self.VELOCITY_UP_DOWN = -DRONE_SPEED
        elif key == self.KEY_ROTATE_LEFT:
            self.VELOCITY_YAW = -DRONE_SPEED
        elif key == self.KEY_ROTATE_RIGHT:
            self.VELOCITY_YAW = DRONE_SPEED

    def keyup(self, key):
        """ Set RC channel variables from key release, we use standard 4-channel control
        Arguments:
            key: pygame key
        """
        if key == self.KEY_TAKEOFF:
            self.DRONE.takeoff()
            self.DRONE_SEND_RC_COMMAND = True
        elif key == self.KEY_LANDING:
            self.DRONE.land()
            self.DRONE_SEND_RC_COMMAND = False
        else:
            if key == self.KEY_FORWARD or key == self.KEY_BACKWARD:
                self.VELOCITY_FORWARD_BACK = 0
            elif key == self.KEY_LEFT or key == self.KEY_RIGHT:
                self.VELOCITY_LEFT_RIGHT = 0
            elif key == self.KEY_UP or key == self.KEY_DOWN:
                self.VELOCITY_UP_DOWN = 0
            elif key == self.KEY_ROTATE_LEFT or self.KEY_ROTATE_RIGHT:
                self.VELOCITY_YAW = 0

    def send_rc_command(self):
        """ Send 4-channel rc command """
        if self.DRONE_SEND_RC_COMMAND is True:
            self.DRONE.rc_command(self.VELOCITY_LEFT_RIGHT,
                                  self.VELOCITY_FORWARD_BACK,
                                  self.VELOCITY_UP_DOWN,
                                  self.VELOCITY_YAW)


dc = DroneController()
dc.DISPLAY_MODE = [300, 300]
dc.run()
