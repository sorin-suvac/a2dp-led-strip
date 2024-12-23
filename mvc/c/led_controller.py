# Copyright (c) 2024 suvacsorin@gmail.com
# All rights reserved.
from log.Logger import Logger


class LedController:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def start_listening(self):
        Logger.info(self.__class__.__name__, "start_listening")
        self.view.start(self.model)

    def stop_listening(self):
        Logger.info(self.__class__.__name__, "stop_listening")
        self.view.stop(self.model)

    def set_mode(self, mode):
        Logger.info(self.__class__.__name__, "set_mode {0}".format(mode))
        self.view.set_mode(self.model, mode)
