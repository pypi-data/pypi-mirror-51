# -*- coding:utf-8 -*-

import logging
import os 
import shutil
import time
import sys
initialized = False
formatter = logging.Formatter('%(asctime)s %(levelname)s %(process)d' '[%(filename)s:%(lineno)d %(funcName)s]: %(message)s')


class Configer():
    def __init__(self):
        self.__log_path = ""
        self.__file_handler = None
        self.__console_handler = None
        self.__pure_path = "./log.txt"
        self.__time_format = "%Y%m%d%H%M"
        self.__time_format = "%Y%m%d"

    inst = None

    @staticmethod
    def get():
        if Configer.inst == None:
            Configer.inst = Configer()
        return Configer.inst

    def set_file_handler(self):
        date_str = time.strftime(self.__time_format)
        self.__log_path = self.__pure_path + '.' + date_str

        fh = logging.FileHandler(self.__log_path)
        fh.setFormatter(formatter)
        self.__file_handler = fh
        logging.getLogger('').addHandler(fh)

    def set_console_handler(self):
        if not self.has_console_handler():
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            console.setFormatter(formatter)
            self.__console_handler = console
            logging.getLogger('').addHandler(console)
            logging.getLogger('').setLevel(logging.INFO)

    def has_console_handler(self):
        return self.__console_handler != None

    def del_console_handler(self):
        logging.getLogger('').removeHandler(self.__console_handler)
        del self.__console_handler
        self.__console_handler = None

    def del_file_handler(self):
        logging.getLogger('').removeHandler(self.__file_handler)
        del self.__file_handler
        self.__file_handler = None

    def rotate(self):
        date_str = time.strftime(self.__time_format)
        path = self.__pure_path + '.' + date_str
        self.__log_path

        if path == self.__log_path:
            return
        sys.stdout.flush()
        sys.stderr.flush()
        self.del_file_handler()
        self.set_file_handler()

    def init(self, level, path="./log.txt", quiet=False):
        self.__pure_path = path
        if quiet:
            self.del_console_handler()

        if not quiet and not self.has_console_handler():
            self.set_console_handler()
        self.set_file_handler()

        cmd = str("logging.getLogger("").setLevel(logging.%s)" % (level.upper()))
        exec cmd


class Logger():
    def __init__(self, elk=False, hosts=None, topic=None):
        self.elk = elk
        if self.elk:
            self.hosts = hosts
            self.topic = topic
        if not Configer.get().has_console_handler():
            Configer.get().set_console_handler()
        #self.info = logging.info
        #self.debug = logging.debug
        #self.warning = logging.warning
        #self.error = logging.error
        #self.critical = logging.critical
        #Configer.get().del_console_handler()

    def info(self, msg, *args, **kwargs):
        if self.elk:
            log_elk(self.hosts, self.topic, msg % args, level='INFO')
        logging.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        if self.elk:
            log_elk(self.hosts, self.topic, msg % args, level='DEBUG')
        logging.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.elk:
            log_elk(self.hosts, self.topic, msg % args, level='WARNING')
        logging.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.elk:
            log_elk(self.hosts, self.topic, msg % args, level='ERROR')
        logging.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.elk:
            log_elk(self.hosts, self.topic, msg % args, level='CRITICAL')
        logging.critical(msg, *args, **kwargs)


def log_elk(hosts, topic, msg, level='INFO'):
    try:
        from kafka_utils import kafka_produce
        formatter = '{level} {ip} {process}[{filename}:{lineno} {funcName}]: {message}'

        rv = findCaller()

        msg = formatter.format(
                ip=get_host_ip(), level=level, process=os.getpid(),
                filename=rv[0], lineno=rv[1], funcName=rv[2],
                message=msg)
        kafka_produce(hosts, topic, bytes(msg))
    except:
        logging.info('fail to log elk of hosts: [%s], topic: [%s]', 
            hosts, topic)
        import traceback
        err_msg = traceback.format_exc()
        logging.error(err_msg)


def get_host_ip():
    import socket
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip


def currentframe():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        return sys.exc_info()[2].tb_frame.f_back


def get_srcfile():
    if hasattr(sys, 'frozen'): #support for py2exe
        _srcfile = "logging%s__init__%s" % (os.sep, __file__[-4:])
    elif __file__[-4:].lower() in ['.pyc', '.pyo']:
        _srcfile = __file__[:-4] + '.py'
    else:
        _srcfile = __file__
    _srcfile = os.path.normcase(_srcfile)
    return _srcfile


_srcfile = get_srcfile()


def findCaller():
    """Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
    """
    f = currentframe()
    if f is not None:
        f = f.f_back
    rv = "(unknown file)", 0, "(unknown function)"
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if filename == _srcfile:
            f = f.f_back
            continue
        rv = (co.co_filename, f.f_lineno, co.co_name)
        break
    return rv


def log_init(level, path="./log.txt", quiet=False, 
        elk=False, hosts=None, topic=None):
    global initialized
    if initialized: return
    Configer.get().init(level, path, quiet)
    
    if elk:
        global g_logger
        g_logger = Logger(elk, hosts, topic)
    #initialized = True


g_logger = Logger()


def logger():
    Configer.get().rotate()
    return g_logger


def log(log_dir, log_level='info', quiet=False, elk=False, hosts=None, topic=None):
    def decorator(func):
        def wrapper(*args, **kw):
            log_init(log_level, log_dir, quiet=quiet, elk=elk, hosts=hosts, topic=topic)
            return func(*args, **kw)
        return wrapper
    return decorator


if __name__ == '__main__':
    @log('./log2.txt', elk=False, hosts='dev-01:9092,dev-02:9092,dev-03:9092', topic='elk-logstash-dev')
    def f():
        logger().info('fffffff')

    log_init('info', './log.txt', quiet=False, 
            elk=False, hosts='dev-01:9092,dev-02:9092,dev-03:9092', topic='elk-logstash-dev')
    log_init('info', './log.txt', quiet=False, 
            elk=False, hosts='dev-01:9092,dev-02:9092,dev-03:9092', topic='elk-logstash-dev')
    while True:
        l = logger()
        import random
        l.info('info:abc, %s, %s, %s', 
                random.randint(1, 1000),
                random.randint(1, 1000),
                random.randint(1, 1000))

        l.info("info:abc, [%s], %s, %s" % ( 
                random.randint(1, 1000),
                random.randint(1, 1000),
                random.randint(1, 1000)))
        f()
        #l.error('error:abc')
        #l.debug('debug:abc')
        time.sleep(1)


