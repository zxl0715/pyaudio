import configparser
import inspect
import os

import loggingHandler
from collections import Iterable

cf = configparser.ConfigParser()
"""conf.ini  （ini，conf）"""
try:

    this_file = inspect.getfile(inspect.currentframe())
    dirpath = os.path.abspath(os.path.dirname(this_file))
    cf.read(os.path.join(dirpath, 'conf/app.conf'), encoding="utf-8-sig")
except Exception as e:
    loggingHandler.logger.exception('错误代码：10001 读取配置文件失败，请检查应用程序配置文件信息！')


def get_logging_level():
    """日志等级 （NOTSET ; DEBUG ; INFO ; WARNING ; ERROR ;CRITICAL）"""
    return cf.get('logginConfig', 'LoggingLevel')

def get_record_seconds():
    """#录音时间 单位秒"""
    return cf.getint('config', 'record_seconds')

def get_disk_size():
    """#当前运行磁盘,允许 最小剩余空间多少GB"""
    return cf.getint('config', 'disk_size')
