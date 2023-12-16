# encoding: utf-8

import logging
import configparser
import os
import frozen


def get_logger(name):
    frozen_path = frozen.get_frozen_path()
    cf = configparser.RawConfigParser()
    filename = os.path.join(frozen_path, "config", "logger.ini")
    cf.read(filename, encoding="utf-8")
    cf.options("config")
    level = cf.get("config", "level")
    path = cf.get("config", "path")
    log_format = cf.get("config", "format")
    if not level:
        level = logging.INFO
    else:
        level = str(level)
        if level.upper() == "NOTSET":
            level = logging.NOTSET
        elif level.upper() == "DEBUG":
            level = logging.DEBUG
        elif level.upper() == "INFO":
            level = logging.INFO
        elif level.upper() == "WARN":
            level = logging.WARN
        elif level.upper() == "ERROR":
            level = logging.ERROR
        elif level.upper() == "FATAL":
            level = logging.FATAL
        else:
            level = logging.INFO
    logging.basicConfig(level=level, format=log_format)
    filename = os.path.join(frozen_path, path)
    log_folder = os.path.dirname(filename)
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    handler = logging.FileHandler(filename=filename, encoding="utf-8")
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    return logger
