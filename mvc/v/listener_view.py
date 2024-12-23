# Copyright (c) 2024 suvacsorin@gmail.com
# All rights reserved.
import struct
import threading

import numpy as np
import pyaudio

from log.Logger import Logger


class ListenerView:

    def __init__(self):
        self.__stop_event = threading.Event()
        self.__thread = None
        self.__pyaudio = None
        self.__accuracy = 64
        self.__chunk_size = 1024
        self.__frequency = 10
        self.__sample_rate = None

    def start(self, leds):
        Logger.info(self.__class__.__name__, "start")
        if self.__stop_event.is_set():
            self.__stop_event.clear()
        if self.__thread is None or not self.__thread.is_alive():
            self.__thread = threading.Thread(target=self.__run, args=(leds,))
            self.__thread.start()

    def stop(self, leds):
        Logger.info(self.__class__.__name__, "stop")
        self.__stop_event.set()
        self.turn_off_leds(leds)

    def __init_stream(self):
        Logger.info(self.__class__.__name__, "init_stream")
        device_index = None
        device_info = None
        channels = None
        self.__pyaudio = pyaudio.PyAudio()
        for i in range(self.__pyaudio.get_device_count()):
            device_info = self.__pyaudio.get_device_info_by_index(i)
            channels = device_info['maxInputChannels']
            if channels > 0:
                device_index = i
                break
        self.__sample_rate = int(device_info['defaultSampleRate'])
        stream = self.__pyaudio.open(format=pyaudio.paInt16,
                                     channels=channels,
                                     rate=self.__sample_rate,
                                     input=True,
                                     input_device_index=device_index,
                                     frames_per_buffer=self.__chunk_size)
        return stream

    def __run(self, leds):
        Logger.info(self.__class__.__name__, "run")
        for led in leds:
            led.init_pigpio()
        self.turn_off_leds(leds)
        stream = self.__init_stream()
        data = stream.read(self.__chunk_size)
        frames = self.__sample_rate
        while not self.__stop_event.is_set() and data != '':
            data = stream.read(self.__chunk_size)
            data_int = np.array(struct.unpack(str(64 * self.__chunk_size) + 'B', data), dtype='b')[::self.__accuracy]
            if frames % self.__frequency == 0:
                for led in leds:
                    led.next_val = led.get_led_value(data_int)
                    for val in range(led.current_val, led.next_val, 1):
                        led.set_value(val)
                    led.current_val = led.next_val
            frames = frames - 1
        self.turn_off_leds(leds)
        stream.stop_stream()
        stream.close()
        self.__pyaudio.terminate()

    @staticmethod
    def set_mode(leds, mode):
        Logger.info("static", "init_stream")
        for led in leds:
            led.set_mode(mode)

    @staticmethod
    def turn_off_leds(leds):
        Logger.info("static", "init_stream")
        for led in leds:
            led.set_value(0)
