# Copyright (c) 2024 suvacsorin@gmail.com
# All rights reserved.
class Logger:

    @staticmethod
    def info(tag, msg):
        print("INFO. {0}: {1}".format(tag, msg))

    @staticmethod
    def err(tag, msg):
        print("ERROR. {0}: {1}".format(tag, msg))
