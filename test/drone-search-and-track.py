from lib.drone.ryze_tello import Drone
import pygame
import numpy as np
import time
import cv2
import sys

DRONE_SPEED = 60


class SeekAcquireTrack(object):
    # +--------------------------------------------------------------+
    # Keymaps
    # +--------------------------------------------------------------+
    KEY_TAKEOFF = pygame.K_t
    KEY_LANDING = pygame.K_l

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
    DRONE = None
    YAW_DIRECTION = 'left'
    YAW_VELOCITY = 0
    IS_FLYING = False
    IS_OBJECT_DETECTED = False

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Video Stream")
        self.screen = pygame.display.set_mode(self.DISPLAY_MODE)

        # Instantiate drone object
        self.DRONE = Drone()

        # self.DRONE.speed(30)

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // self.DISPLAY_FPS)

        cascade_file = sys.path[1] + "/data/haarcascades/haarcascade_frontalface_default.xml"
        self.object_cascade = cv2.CascadeClassifier(cascade_file)

    def run(self):

        # Initiate connection to drone object
        self.DRONE.hello()

        # Print drone stats
        self.DRONE.info()

        # Start video streaming
        self.DRONE.start_video_streaming()

        frame_read = self.DRONE.get_video_frames()
        should_stop = False
        idx = 0
        while not should_stop:

            if self.DRONE.is_low_battery is True:
                print('Low battery')
                break

            if self.IS_FLYING is True:
                if self.IS_OBJECT_DETECTED is False:
                    if idx < 160:
                        idx = idx + 1
                        if self.YAW_DIRECTION is 'left':
                            # self.DRONE.rc_command(0, 0, 0, -DRONE_SPEED)
                            self.DRONE.rotate_left(1)
                        else:
                            # self.DRONE.rc_command(0, 0, 0, DRONE_SPEED)
                            self.DRONE.rotate_right(1)
                    else:
                        idx = 0
                        if self.YAW_DIRECTION is 'left':
                            self.YAW_DIRECTION = 'right'
                        elif self.YAW_DIRECTION is 'right':
                            print('Where are you?')
                            time.sleep(5)

            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == self.KEY_TAKEOFF:
                        self.IS_FLYING = True
                        self.DRONE.takeoff(20)
                    elif event.key == self.KEY_LANDING:
                        self.IS_FLYING = False
                        self.DRONE.land()
                        break

            if frame_read.stopped:
                break

            self.screen.fill([0, 0, 0])

            # Single frame
            frame = frame_read.frame

            # +--------------------------------------------------------------+
            # Object detection
            # +--------------------------------------------------------------+
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.object_cascade.detectMultiScale(gray, 1.3, 5)

            amount_detect = len(faces)
            if self.IS_OBJECT_DETECTED is False and amount_detect != 0:
                self.IS_OBJECT_DETECTED = True

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                # roi_gray = gray[y:y + h, x:x + w]
                # roi_color = frame[y:y + h, x:x + w]

            # +--------------------------------------------------------------+
            # Drone stats
            # +--------------------------------------------------------------+
            txt_stats = "Bat: {battery}%, Temp: {temp}C, Alt: {alt}cm".format(
                battery=str(self.DRONE.get_battery()),
                temp=str(int(self.DRONE.get_temperature())),
                alt=str(self.DRONE.get_altitude()))
            cv2.putText(frame, txt_stats, (5, 720 - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)

            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()
            time.sleep(1 / self.DISPLAY_FPS)

        # Call it always before finishing. To deallocate resources.
        self.DRONE.bye()
        sys.exit()


dc = SeekAcquireTrack()
dc.DISPLAY_MODE = [300, 300]
dc.run()
