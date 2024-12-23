# Copyright (c) 2024 suvacsorin@gmail.com
# All rights reserved.
import json
import os
from http.client import HTTPException
from http.server import CGIHTTPRequestHandler

from log.Logger import Logger
from mvc.c.led_controller import LedController
from mvc.m.led_model import Led
from mvc.v.listener_view import ListenerView


class RequestHandler(CGIHTTPRequestHandler):

    __HTML_INDEX = "/{0}/../res/index.html".format(os.path.dirname(os.path.abspath(__file__)))

    __leds = [Led(pin=17, color=Led.RED), Led(pin=22, color=Led.GREEN), Led(pin=27, color=Led.BLUE)]
    __listener_view = ListenerView()
    __led_controller = LedController(__leds, __listener_view)

    def do_GET(self):
        match self.path:
            case '/':
                self.path = self.__HTML_INDEX
                self.__show_main()
            case _:
                Logger.err(self.__class__.__name__, "{0} not found".format(self.path))
                self.__show_error(404)

    def do_POST(self):
        request_payload = self.__get_payload_as_dict()
        key = request_payload.get('key', 'not found')
        if key is None:
            Logger.err(self.__class__.__name__, "key is None")
            self.__show_error(500)
            return
        match self.path:
            case '/display':
                self.__display(key)
            case '/mode':
                self.__update_mode(key)
            case _:
                Logger.err(self.__class__.__name__, "{0} not found".format(self.path))
                self.__show_error(404)

    def __get_payload_as_dict(self):
        data = None
        content_length = int(self.headers['Content-Length'])
        raw_data = self.rfile.read(content_length)
        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError as err:
            Logger.err(self.__class__.__name__, err)
            self.__show_error(500)
        return data

    def __show_main(self):
        try:
            html_file = open(self.path[1:]).read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(html_file, 'utf-8'))
        except OSError as err:
            Logger.err(self.__class__.__name__, err)
            self.__show_error(500)
        
    def __show_error(self, err_code):
        err_msg = 'Error'
        match err_code:
            case 404:
                err_msg = '404 - Not Found'
            case 500:
                err_msg = '500 - Internal Server Error'
        self.send_response(err_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(err_msg.encode('utf-8')))

    def __update_mode(self, mode):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.__led_controller.set_mode(mode)
        except HTTPException as err:
            Logger.err(self.__class__.__name__, err)
            self.__show_error(500)

    def __display(self, bt):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            if bt == '1':
                self.__led_controller.start_listening()
            else:
                self.__led_controller.stop_listening()
        except HTTPException as err:
            Logger.err(self.__class__.__name__, err)
            self.__show_error(500)
