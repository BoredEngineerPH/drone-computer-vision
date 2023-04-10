from lib.drone.ryze_tello import Drone
import pygame
import numpy as np
import time

# Speed of the drone
# 无人机的速度
S = 60
# Frames per second of the pygame window display
# A low number also results in input lag, as input information is processed once per frame.
# pygame窗口显示的帧数
# 较低的帧数会导致输入延迟，因为一帧只会处理一次输入信息
FPS = 120


class DroneController(object):
    """ Maintains the Tello display and moves it through the keyboard keys.
        Press escape key to quit.
        The controls are:
            - T: Takeoff
            - L: Land
            - Arrow keys: Forward, backward, left and right.
            - A and D: Counter clockwise and clockwise rotations (yaw)
            - W and S: Up and down.

        保持Tello画面显示并用键盘移动它
        按下ESC键退出
        操作说明：
            T：起飞
            L：降落
            方向键：前后左右
            A和D：逆时针与顺时针转向
            W和S：上升与下降

    """

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
    DRONE_SPEED = 60
    DRONE_SEND_RC_CONTROL = False

    # Drone velocities between -100~100
    VELOCITY_LEFT_RIGHT = 0
    VELOCITY_UP_DOWN = 0
    VELOCITY_YAW = 0

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Video Stream")
        if self.DISPLAY_MODE == 'fullscreen':
            self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.DISPLAY_MODE)

        # Instantiate drone object
        self.DRONE = Drone()

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // self.DISPLAY_FPS)

    def run(self):

        self.DRONE.hello()

        # In case streaming is on. This happens when we quit this program without the escape key.
        # 防止视频流已开启。这会在不使用ESC键退出的情况下发生。
        self.tello.streamoff()
        self.tello.streamon()

        frame_read = self.tello.get_frame_read()

        should_stop = False
        while not should_stop:

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    should_stop = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        should_stop = True
                    else:
                        self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup(event.key)

            if frame_read.stopped:
                break

            self.screen.fill([0, 0, 0])

            frame = frame_read.frame
            # battery n. 电池
            text = "Battery: {}%".format(self.tello.get_battery())
            cv2.putText(frame, text, (5, 720 - 5),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)

            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()

            time.sleep(1 / FPS)

        # Call it always before finishing. To deallocate resources.
        # 通常在结束前调用它以释放资源
        self.tello.end()

    def keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key

        基于键的按下上传各个方向的速度
        参数：
            key：pygame事件循环中的键事件
        """
        if key == pygame.K_UP:  # set forward velocity
            self.for_back_velocity = S
        elif key == pygame.K_DOWN:  # set backward velocity
            self.for_back_velocity = -S
        elif key == pygame.K_LEFT:  # set left velocity
            self.left_right_velocity = -S
        elif key == pygame.K_RIGHT:  # set right velocity
            self.left_right_velocity = S
        elif key == pygame.K_w:  # set up velocity
            self.up_down_velocity = S
        elif key == pygame.K_s:  # set down velocity
            self.up_down_velocity = -S
        elif key == pygame.K_a:  # set yaw counter clockwise velocity
            self.yaw_velocity = -S
        elif key == pygame.K_d:  # set yaw clockwise velocity
            self.yaw_velocity = S

    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key

        基于键的松开上传各个方向的速度
        参数：
            key：pygame事件循环中的键事件
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            not self.tello.land()
            self.send_rc_control = False

    def update(self):
        """ Update routine. Send velocities to Tello.

            向Tello发送各方向速度信息
        """
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity,
                self.up_down_velocity, self.yaw_velocity)


def main():
    dc = DroneController()

    # run frontend

    dc.run()


if __name__ == '__main__':
    main()