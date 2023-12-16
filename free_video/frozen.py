# encoding: utf-8

import sys
import os


def get_frozen_path():
    if hasattr(sys, "frozen"):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(__file__)
