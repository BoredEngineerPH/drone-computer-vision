from controller.rclib import RClib
from controller.mode.mode2 import Keymap
from drone.ryze_tello import Drone


class DroneController:

    RC = None  # Remote control library
    DRONE = None  # Drone object instance

    # Drone Speed and Velocity values
    VELOCITY_FORWARD_BACK = 0
    VELOCITY_LEFT_RIGHT = 0
    VELOCITY_UP_DOWN = 0
    VELOCITY_YAW = 0
    DRONE_SPEED = 10

    SEND_RC_CONTROL = False

    def run(self):
        self.VELOCITY_UP_DOWN = 20
        # Initialize Remote control library which uses pygame
        self.RC = RClib()

        # Initialize drone object
        self.DRONE = Drone()

        # Connect to drone
        self.DRONE.connect()

        # Load keymaps or stick mode
        self.RC.keymap(Keymap())

        # Set callback functions
        self.RC.set_event_keyup(self.keyup_callback)
        self.RC.set_event_keydown(self.keydown_callback)
        self.RC.set_event_update(self.update_callback)
        self.RC.run()
        self.DRONE.hello().end()

    def keyup_callback(self, event):
        if event.key == self.RC.KEYMAPS.THROTTLE_UP or event.key == self.RC.KEYMAPS.THROTTLE_DOWN:
            self.update_callback()
            self.VELOCITY_UP_DOWN = 0
        elif event.key == self.RC.KEYMAPS.YAW_LEFT or event.key == self.RC.KEYMAPS.YAW_RIGHT:
            self.update_callback()
            self.VELOCITY_YAW = 0
        elif event.key == self.RC.KEYMAPS.PITCH_UP or event.key == self.RC.KEYMAPS.PITCH_DOWN:
            self.update_callback()
            self.VELOCITY_FORWARD_BACK = 0
        elif event.key == self.RC.KEYMAPS.ROLL_LEFT or event.key == self.RC.KEYMAPS.ROLL_RIGHT:
            self.update_callback()
            self.VELOCITY_LEFT_RIGHT = 0
        elif event.key == self.RC.KEYMAPS.TAKEOFF:
            self.DRONE.take_off()
            print('Taking off..')
            self.SEND_RC_CONTROL = True
        elif event.key == self.RC.KEYMAPS.LAND:
            print('Landing..')
            self.DRONE.land()
            self.SEND_RC_CONTROL = False

    def keydown_callback(self, event):

        if event.key == self.RC.KEYMAPS.THROTTLE_UP:
            self.VELOCITY_UP_DOWN = self.DRONE_SPEED
        elif event.key == self.RC.KEYMAPS.THROTTLE_DOWN:
            self.VELOCITY_UP_DOWN = -self.DRONE_SPEED
        elif event.key == self.RC.KEYMAPS.YAW_LEFT:
            self.VELOCITY_YAW = -self.DRONE_SPEED
        elif event.key == self.RC.KEYMAPS.YAW_RIGHT:
            self.VELOCITY_YAW = self.DRONE_SPEED
        elif event.key == self.RC.KEYMAPS.PITCH_UP:
            self.VELOCITY_FORWARD_BACK = self.DRONE_SPEED
        elif event.key == self.RC.KEYMAPS.PITCH_DOWN:
            self.VELOCITY_FORWARD_BACK = -self.DRONE_SPEED
        elif event.key == self.RC.KEYMAPS.ROLL_LEFT:
            self.VELOCITY_LEFT_RIGHT = -self.DRONE_SPEED
        elif event.key == self.RC.KEYMAPS.ROLL_RIGHT:
            self.VELOCITY_LEFT_RIGHT = self.DRONE_SPEED

    def update_callback(self):
        if self.SEND_RC_CONTROL is True:
            print(self.DRONE_SPEED)
            print(self.VELOCITY_UP_DOWN)
            print(self.VELOCITY_LEFT_RIGHT)
            print(self.VELOCITY_FORWARD_BACK)
            print(self.VELOCITY_YAW)
            self.DRONE.hello().send_rc_control(self.VELOCITY_LEFT_RIGHT, self.VELOCITY_FORWARD_BACK,
                                               self.VELOCITY_UP_DOWN, self.VELOCITY_YAW)


dc = DroneController()
dc.run()
