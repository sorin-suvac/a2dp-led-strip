# Copyright (c) 2024 suvacsorin@gmail.com
# All rights reserved.
from http.server import HTTPServer

from web.server.request_handler import RequestHandler

if __name__ == "__main__":
    webServer = HTTPServer(('0.0.0.0', 8080), RequestHandler)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')

    webServer.server_close()
