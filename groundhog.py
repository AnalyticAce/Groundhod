#!/usr/bin/env python3

from source.wizard import GroundhogError, Groundhog
from sys import exit, stdout

if __name__ == '__main__':
    try:
        Groundhog().run()
    except GroundhogError as e:
        stdout.write(str(type(e).__name__) + ": {}\n".format(e))
        exit(84)
