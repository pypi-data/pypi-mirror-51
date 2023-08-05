import datetime
import logging
import os
import __main__


def getLogDir():
    if 'LOG_DIR' not in os.environ:
        log_dir = os.path.join(os.getcwd(), 'log', datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d'))
    else:
        log_dir = os.path.join(os.environ['LOG_DIR'], datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d'))
    try:
        os.makedirs(log_dir)
    except FileExistsError:
        pass
    return log_dir


def getLogFile():
    if('__file__' in __main__.__dict__):
        log_file = os.path.splitext(os.path.basename(__main__.__file__))[0] + '.log'
    else:
        log_file = 'python.log'
    return log_file


def init(logDir = getLogDir(), logFile = getLogFile(), debugOn = True):
    logFile = os.path.join(logDir, logFile)
    if debugOn:
        logLevel = logging.DEBUG
    else:
        logLevel = logging.INFO
    logging.basicConfig(filename = logFile, level = logLevel,
                        format = '%(asctime)s.%(msecs)d %(levelname)-5s [%(pathname)s:%(lineno)d] %(message)s',
                        datefmt = '%H:%M:%S')

