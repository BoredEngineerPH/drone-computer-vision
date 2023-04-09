import pygame
import sys
import time


class RClib:

    # pygame screen options
    DISPLAY_MODE_FULLSCREEN = False
    DISPLAY_MODE_SIZE = (300, 300)

    # Frames per second of the pygame window display
    # A low number also results in input lag, as input information is processed once per frame.
    FPS = 120

    KEYMAPS = None  # We use DJI official stick mode mapping

    # Event callback events
    EVENT_KEYUP = None
    EVENT_KEYDOWN = None
    EVENT_UPDATE = None

    def keymap(self, keymap):
        """Load controller stick map also known as Stick Mode
        Parameters:
            keymap: array
        """
        if keymap is not None:
            self.KEYMAPS = keymap

    def set_event_keyup(self, callback_func):
        """Set event keyup
        Parameters:
            callback_func: callable
        """
        if callable(callback_func) is True:
            self.EVENT_KEYUP = callback_func

    def set_event_keydown(self, callback_func):
        """Set event keydown
        Parameters:
            callback_func: callable
        """
        if callable(callback_func) is True:
            self.EVENT_KEYDOWN = callback_func

    def set_event_update(self, callback_func):
        """Set event update
        Parameters:
            callback_func: callable
        """
        if callable(callback_func) is True:
            self.EVENT_UPDATE = callback_func

    def run(self):
        pygame.init()
        if self.DISPLAY_MODE_FULLSCREEN is True:
            display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            display = pygame.display.set_mode(self.DISPLAY_MODE_SIZE)

        stop_loop = False
        while not stop_loop:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == self.KEYMAPS.QUIT:
                        stop_loop = True
                    if callable(self.EVENT_KEYDOWN):
                        self.EVENT_KEYDOWN(event)
                elif event.type == pygame.KEYUP:
                    if callable(self.EVENT_KEYUP):
                        self.EVENT_KEYUP(event)

            pygame.display.update()
            time.sleep(1 / self.FPS)
