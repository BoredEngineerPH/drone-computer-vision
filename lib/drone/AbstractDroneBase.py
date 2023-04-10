"""Drone object library

This class standardized the implementation of drone control
"""

# coding=utf-8

from abc import ABC, abstractmethod
import logging


class AbstractDroneBase(ABC):
    # +--------------------------------------------------------------+
    # DEFAULT OBJECT VARIABLES
    # +--------------------------------------------------------------+
    DRONE_SPEED = 10  # Speed of your drone
    MIN_TAKE_OFF_HEIGHT = 70  # Lowest take-off height of drone, anything below this will not be applied
    LOW_BATT_THRESHOLD = 10  # Lowest battery percent anything below it will not fly
    HIGH_TEMP_THRESHOLD = 80.0  # Highest temperature (HOT) anything above it will not fly, value in Celsius
    LOW_TEMP_THRESHOLD = 5.0  # Lowest temperature (COLD) anything below it will not fly, value in Celsius

    # +--------------------------------------------------------------+
    # LOG MESSAGES
    # +--------------------------------------------------------------+
    LOGM_NOT_CONNECTED = 'You are not connected to the drone.'
    LOGM_ALREADY_FLYING = 'You are already flying.'
    LOGM_LOWBAT = 'Battery too low, please charge.'
    LOGM_HOT = 'Drone is overheating, please cool it down in room temperature and try again.'
    LOGM_COLD = 'Drone is too cold to start.'
    LOGM_KILL = 'Sending call signal to aircraft to stop all motors.'

    # +--------------------------------------------------------------+
    # PRIVATE VARIABLES
    # +--------------------------------------------------------------+
    __NAME = None  # Name of object
    __LOGGER = None  # Logger instance

    # +--------------------------------------------------------------+
    # Private conditional flags
    # +--------------------------------------------------------------+
    __IS_CONNECTED = False
    __IS_FLYING = False
    __IS_LOWBAT = False
    __IS_HOT = False
    __IS_COLD = False
    __IS_SAFE_TO_LAND = True
    __NO_VIDEO_STREAM = False  # If set to True that means aircraft allows video stream

    # +--------------------------------------------------------------+
    # Telemetry
    # +--------------------------------------------------------------+
    __TELEMETRY_BATTERY_PERC = 0
    __TELEMETRY_AVERAGE_TEMP = 0
    __TELEMETRY_HIGH_TEMP = 0
    __TELEMETRY_LOW_TEMP = 0
    __TELEMETRY_ALTITUDE = 0
    __TELEMETRY_DRONE_FIRMWARE_VERSION = 0

    def setup(self, name):
        """Pre-setup
        Arguments:
            name: string
        """
        self.__NAME = name

        # Instantiate logger
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('[%(levelname)s] %(filename)s - %(lineno)d - %(message)s'))
        self.__LOGGER = logging.getLogger(name)
        self.__LOGGER.addHandler(handler)
        self.__LOGGER.setLevel(logging.INFO)

    def log(self, message):
        """Print log message to logger"""
        self.__LOGGER.info(message)

    def closing(self):
        """Reset all variables """
        self.__IS_CONNECTED = False
        self.__IS_FLYING = False
        self.__IS_LOWBAT = False
        self.__IS_HOT = False
        self.__IS_COLD = False
        self.__IS_SAFE_TO_LAND = True
        self.__NO_VIDEO_STREAM = False
        self.__TELEMETRY_BATTERY_PERC = 0
        self.__TELEMETRY_AVERAGE_TEMP = 0
        self.__TELEMETRY_HIGH_TEMP = 0
        self.__TELEMETRY_LOW_TEMP = 0
        self.__TELEMETRY_ALTITUDE = 0
        self.__TELEMETRY_DRONE_FIRMWARE_VERSION = 0

    # +--------------------------------------------------------------+
    # Conditional Statements
    # +--------------------------------------------------------------+
    @property
    def can_we_fly(self):
        """Pre-flight check if the drone is capable of flying
        this also ensure that the drone will not get damage
        Return:
            boolean
        """
        if self.is_connected is not True:
            self.log(self.LOGM_NOT_CONNECTED)
            return False
        elif self.is_flying is True:
            self.log(self.LOGM_ALREADY_FLYING)
            return False
        elif self.is_low_battery is True:
            self.log(self.LOGM_LOWBAT)
            return False
        elif self.is_over_heating is True:
            self.log(self.LOGM_HOT)
            return False
        elif self.is_cold is True:
            self.log(self.LOGM_COLD)
            return False
        else:
            return True

    @property
    def can_we_land(self):
        """Pre-landing checklists to check there is no obstraction when landing
        the aircraft
        Return:
            boolean
        """
        # This method is optional but usefull when you want to have
        # safe landing features, thus preventing damage to the aircraft
        return self.__IS_SAFE_TO_LAND

    # +--------------------------------------------------------------+
    # Telemetry
    # +--------------------------------------------------------------+
    def set_telemetry(self, telemetry, value):
        """Set telemetry value
        Parameters:
            telemetry: string
            value: any
        """
        if telemetry == 'battery':
            self.__TELEMETRY_BATTERY_PERC = value
        if telemetry == 'altitude':
            self.__TELEMETRY_ALTITUDE = value
        if telemetry == 'average_temp':
            self.__TELEMETRY_AVERAGE_TEMP = value
        if telemetry == 'high_temp':
            self.__TELEMETRY_HIGH_TEMP = value
        if telemetry == 'low_temp':
            self.__TELEMETRY_LOW_TEMP = value
        if telemetry == 'drone_firmware_version':
            self.__TELEMETRY_DRONE_FIRMWARE_VERSION = value

    @abstractmethod
    def update_telemetry(self):
        """Update all telemetry"""
        pass

    def info(self):
        """Prints drone information
        """
        print('+--------------------------------------------------------------+')
        info = "Aircraft : {aircraft}, Firmware : {firmware}".format(aircraft=self.__NAME, firmware=str(self.__TELEMETRY_DRONE_FIRMWARE_VERSION))
        print(info)

        battery = str(self.__TELEMETRY_BATTERY_PERC)+'%'
        average_temp = str(self.__TELEMETRY_AVERAGE_TEMP)+'°C'
        high_temp = str(self.__TELEMETRY_HIGH_TEMP)+'°C'
        low_temp = str(self.__TELEMETRY_LOW_TEMP)+'°C'
        altitude = str(self.__TELEMETRY_ALTITUDE)+'cm'
        info = "Battery : {battery}, Altitude : {altitude}".format(battery=battery, altitude=altitude)
        print(info)

        info = "Average Temperature : {average_temp}, Highest Temp : {high_temp}, Lowest Temp : {low_temp}".format(average_temp=average_temp, high_temp=high_temp, low_temp=low_temp)
        print(info)
        print('+--------------------------------------------------------------+')

    # +--------------------------------------------------------------+
    # Flag setter and conditional methods
    # +--------------------------------------------------------------+
    def im_connected(self, x: bool):
        """Set __IM_CONNECTED flag
        Parameters:
            x: bool
        """
        self.__IS_CONNECTED = x

    @property
    def is_connected(self):
        """Check if we are already connected to the drone object
        Return:
            boolean
        """
        return self.__IS_CONNECTED

    def im_fying(self, x: bool):
        """Set __IM_FLYING flag
        Parameters:
            x: bool
        """
        self.__IS_FLYING = x

    @property
    def is_flying(self):
        """Check if we are already flying
        Return:
            boolean
        """
        return self.__IS_FLYING

    @property
    def is_low_battery(self):
        """Check if drone is low battery
        Return:
            boolean
        """
        if self.__TELEMETRY_BATTERY_PERC < self.LOW_BATT_THRESHOLD:
            return True
        else:
            return False

    @property
    def is_over_heating(self):
        """Check if drone is overheating
        Return:
            boolean
        """
        if self.__TELEMETRY_HIGH_TEMP > self.HIGH_TEMP_THRESHOLD:
            return True
        else:
            return False

    @property
    def is_cold(self):
        """Check if drone is too cold to function
        Return:
            boolean
        """
        if self.__TELEMETRY_LOW_TEMP < self.LOW_TEMP_THRESHOLD:
            return True
        else:
            return False

    def i_can_land(self, x: bool):
        """Set __IS_SAFE_TO_LAND flag
        Parameters:
            x: bool
        """
        self.__IS_SAFE_TO_LAND = x

    @property
    def can_land(self):
        """Check if drone is safe to land
        Return:
            boolean
        """
        return self.__IS_SAFE_TO_LAND

    def im_video_streaming(self, x: bool):
        """Set __NO_VIDEO_STREAM flag
        Parameters:
            x: bool
        """
        self.__NO_VIDEO_STREAM = x

    @property
    def is_video_streaming(self):
        """Check if drone is safe to land
        Return:
            boolean
        """
        return self.__NO_VIDEO_STREAM

    # +--------------------------------------------------------------+
    # Abstract general methods
    # +--------------------------------------------------------------+
    @abstractmethod
    def hello(self):
        """Initiate connection to drone object"""
        pass

    @abstractmethod
    def bye(self):
        """Gracefully terminate drone object
        """
        pass

    @abstractmethod
    def instance(self):
        """Returns drone object"""
        pass

    @abstractmethod
    def kill(self):
        """Kill all motors, be careful in using this command
        as it can damage your drone or hurt someone
        this is only useful if you want to avoid accidental hitting other
        person
        """
        pass

    @abstractmethod
    def restart(self):
        """Restart drone, you may need to reconnect to the AP
        """
        pass

    # +--------------------------------------------------------------+
    # Abstract navigation control methods
    # +--------------------------------------------------------------+
    @abstractmethod
    def speed(self, speed: int):
        """Set speed to speed cm/s.
        Arguments:
            speed: 10-100
        """
        pass

    @abstractmethod
    def takeoff(self, altitude=None):
        """Initial lift/ascend of aircraft depending on the UAV
        intial altitude may defer but can be invoke by an arguments passed to
        drone takeoff event
        Arguments:
            altitude: 20-500
        """
        pass

    @abstractmethod
    def land(self, delay=None):
        """Land the aircraft
        Arguments
            delay: 1-10
        """
        pass

    @abstractmethod
    def ascend(self, v: int):
        """Increase aircraft altitude to y
        This is also called Throttle up/lift on controller term
        Arguments:
            v: 20-500
        """
        pass

    @abstractmethod
    def descend(self, v: int):
        """Decrease aircraft altitude to y
        This is also called Throttle down/landing on controller term
        Arguments:
            v: 20-500
        """
        pass

    @abstractmethod
    def forward(self, v: int):
        """Move the aircraft forward a/k/a Pitch Down
        Arguments:
            v: 20-500
        """
        pass

    @abstractmethod
    def backward(self, v: int):
        """Move the aircraft backward a/k/a Pitch Up
        Arguments:
            v: 20-500
        """
        pass

    @abstractmethod
    def left(self, v: int):
        """Move aircraft to left a/k/a Roll Left
        Arguments:
            v: 20-500
        """
        pass

    @abstractmethod
    def right(self, v: int):
        """Move aircraft to left a/k/a Roll Right
        Arguments:
            v: 20-500
        """
        pass

    @abstractmethod
    def rotate_left(self, v: int):
        """Rotate aircrat counter-clockwise/left a/k/a Yaw Left
        Arguments:
            v: 20-500
        """
        pass

    @abstractmethod
    def rotate_right(self, v: int):
        """Rotate aircrat clockwise/right a/k/a Yaw Right
        Arguments:
            v: 20-500
        """
        pass

    @abstractmethod
    def rc_command(self, roll: int, pitch: int, throttle: int, yaw: int):
        """Send RC command via four channels.
        Arguments:
            roll: -100~100 (left/right)
            pitch: -100~100 (forward/backward)
            throttle: -100~100 (up/down)
            yaw: -100~100 (yaw)
        """
        pass

    # +--------------------------------------------------------------+
    # Abstract video streaming methods
    # +--------------------------------------------------------------+
    @abstractmethod
    def start_video_streaming(self):
        """Start video streaming"""
        pass

    @abstractmethod
    def stop_video_streaming(self):
        """Stop video streaming"""
        pass

    @abstractmethod
    def get_video_frames(self):
        """Get video stream frames"""
        pass

    # +--------------------------------------------------------------+
    # Drone Stats
    # +--------------------------------------------------------------+
    @abstractmethod
    def get_battery(self):
        """Get battery statistics"""
        pass

    @abstractmethod
    def get_temperature(self):
        """Get average temperature"""
        pass

    @abstractmethod
    def get_altitude(self):
        """Get current drone altitude"""
        pass
