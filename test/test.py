from lib.drone.ryze_tello import Drone
import pygame
import numpy as np
import time
import cv2
import sys
import os

# Speed of the drone
# 无人机的速度
S = 60
# Frames per second of the pygame window display
# A low number also results in input lag, as input information is processed once per frame.
# pygame窗口显示的帧数
# 较低的帧数会导致输入延迟，因为一帧只会处理一次输入信息
FPS = 120


class SeekTrack(object):
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
            if frame_read.stopped:
                break

            self.screen.fill([0, 0, 0])

            frame = frame_read.frame
            # convert to gray scale of each frames
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detects faces of different sizes in the input image
            faces = self.object_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                # To draw a rectangle in a face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]

            # Add drone stats to display
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

            time.sleep(1 / FPS)

        # Call it always before finishing. To deallocate resources.
        self.DRONE.bye()


st = SeekTrack()
st.run()
