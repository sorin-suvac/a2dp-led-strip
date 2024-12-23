# Copyright (c) 2024 suvacsorin@gmail.com
# All rights reserved.
import numpy as np
import pigpio

from log.Logger import Logger


class Led:

    RED = 1
    GREEN = 2
    BLUE = 3

    MODE_LIGHT = 'light'
    MODE_MEDIUM = 'medium'
    MODE_HIGH = 'high'

    def __init__(self, pin, color):
        self.__pin = pin
        self.__color = color
        self.__pi = None
        self.__mode = self.MODE_MEDIUM
        self.current_value = 0
        self.next_value = 0

    def init_pigpio(self):
        Logger.info(self.__class__.__name__, "init_pigpio")
        self.__pi = pigpio.pi()

    def get_led_value(self, data):
        match self.__mode:
            case self.MODE_LIGHT:
                delta = 0
            case self.MODE_MEDIUM:
                delta = 75
            case self.MODE_HIGH:
                delta = 150
            case _:
                delta = 0

        r_index = int(len(data) / 3)
        g_index = int(len(data) / 3) * 2
        b_index = int(len(data)) - 1
        r_val = int(np.average(data[0:r_index]) / 2)
        g_val = int(np.average(data[r_index:g_index]) / 2)
        b_val = int(np.average(data[g_index:b_index]) / 2)

        if r_val > g_val and r_val > b_val:
            r_val = r_val + delta
        if g_val > r_val and g_val > b_val:
            g_val = g_val + delta
        if b_val > r_val and b_val > g_val:
            b_val = b_val + delta

        values = [r_val, g_val, b_val]
        for i in range(len(values)):
            if values[i] < 0:
                values[i] = 0
            if values[i] > 255:
                values[i] = 255

        r_val, g_val, b_val = values

        match self.__color:
            case self.RED:
                return r_val
            case self.GREEN:
                return g_val
            case self.BLUE:
                return b_val
            case _:
                return None

    def set_value(self, val):
        self.__pi.set_PWM_dutycycle(self.__pin, val)

    def set_mode(self, mode):
        Logger.info(self.__class__.__name__, "set_mode {0}".format(mode))
        self.__mode = mode
