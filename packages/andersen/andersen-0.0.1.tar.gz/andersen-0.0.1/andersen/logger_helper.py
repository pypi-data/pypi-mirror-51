import logging
import os
from logging import handlers

import toml

from andersen import config
from andersen import exception

DEFAULT_CONF = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'etc/log.toml')
_LOG_CONFIG = {}
_LOGGER_MAP = {}

_LOGGER_CONFIG_COMMON = 'common'

FILE_ENCODING = 'utf-8'


def get_config(logger_key, conf_key, conf):
    """
    获取某个配置信息。如果针对某个配置项没有找到对应的key，则向上一级查找，如果还是没有，则从common中查找，否则配置有误
    :param logger_key: 日志对象的名称
    :param conf_key:  配置项的key
    :param conf: 已有配置
    :return:
    """
    global _LOG_CONFIG
    if conf_key in conf:
        return conf.get(conf_key)
    if conf_key in _LOG_CONFIG.get(logger_key):
        return _LOG_CONFIG.get(logger_key).get(conf_key)
    if conf_key in _LOG_CONFIG.get(_LOGGER_CONFIG_COMMON):
        return _LOG_CONFIG.get(_LOGGER_CONFIG_COMMON).get(conf_key)
    raise exception.ConfigParseException()


def create_std_handler(logger_key, conf):
    """
    创建一个输出到控制台的handler
    :param logger_key: 日志对象的名称
    :param conf: 对应handler的配置项，该项需要能找到如下参数：format, level
    :return:
    """
    handler = logging.StreamHandler()
    formatter_str = get_config(logger_key, 'format', conf)
    formatter = logging.Formatter(formatter_str)
    log_level = get_config(logger_key, 'level', conf)
    log_level = log_level.upper()
    log_level = logging.getLevelName(log_level)
    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    return handler


def create_file_handler(logger_key, conf):
    """
    创建一个输出到文件的handler
    :param logger_key: 日志对象的名称
    :param conf: 对应handler的配置项，该项需要能找到如下参数：format, level, log_file[最好是绝对路径，而且必须包含在conf中]
    :return:
    """
    file_path = conf.get('log_file')
    if not file_path:
        raise exception.ConfigParseException()
    handler = logging.FileHandler(filename=file_path, encoding=FILE_ENCODING)
    formatter_str = get_config(logger_key, 'format', conf)
    formatter = logging.Formatter(formatter_str)
    log_level = get_config(logger_key, 'level', conf)
    log_level = log_level.upper()
    log_level = logging.getLevelName(log_level)
    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    return handler


def create_rotating_handler(logger_key, conf):
    """
    创建一个输出到文件的handler，且文件到达一定大小时会新建新的文件
    :param logger_key: 日志对象的名称
    :param conf: 对应handler的配置项，该项需要能找到如下参数：format, level, max_bytes[单位是bytes，而且必须包含在conf中]
    :return:
    """
    max_bytes = conf.get('max_bytes')
    file_path = conf.get('log_file')
    if not max_bytes or not file_path:
        raise exception.ConfigParseException()

    handler = handlers.RotatingFileHandler(filename=file_path, maxBytes=max_bytes, encoding=FILE_ENCODING)
    formatter_str = get_config(logger_key, 'format', conf)
    formatter = logging.Formatter(formatter_str)
    log_level = get_config(logger_key, 'level', conf)
    log_level = log_level.upper()
    log_level = logging.getLevelName(log_level)
    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    return handler


def create_time_rotating_handler(logger_key, conf):
    """
    创建一个输出到文件的handler，且文件会按照时间rotate
    :param logger_key: 日志对象的名称
    :param conf: 对应handler的配置项，该项需要能找到如下参数：format, level, when[必须包含在conf中]
    :return:
    """
    when = conf.get('when')
    file_path = conf.get('log_file')
    if not when or not file_path:
        raise exception.ConfigParseException()
    handler = handlers.TimedRotatingFileHandler(filename=file_path, when=when)
    formatter_str = get_config(logger_key, 'format', conf)
    formatter = logging.Formatter(formatter_str)
    log_level = get_config(logger_key, 'level', conf)
    log_level = log_level.upper()
    log_level = logging.getLevelName(log_level)
    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    return handler


HANDLER_CREATOR = {
    'std': create_std_handler,
    'file': create_file_handler,
    'rotate': create_rotating_handler,
    'time_rotate': create_time_rotating_handler
}


def load_config(conf=None):
    """
    加载配置文件
    :param conf:
    :return:
    """
    global _LOG_CONFIG
    if conf is None:
        _LOG_CONFIG = config.BASE_CONFIG
    else:   
        configs = []
        if isinstance(conf, str):
            configs.append(conf)
        elif isinstance(conf, list):
            configs.extend(conf)

        _LOG_CONFIG = toml.load(configs)
    _LOG_CONFIG = _LOG_CONFIG.get('log')


def init_logger(logger_key='common'):
    """
    初始化所有日志对象
    :return:
    """
    global _LOG_CONFIG, _LOGGER_MAP
    for k in _LOG_CONFIG:
        log_conf = _LOG_CONFIG.get(k)
        if 'level' not in log_conf:
            raise exception.ConfigParseException()
        level = log_conf.get('level')
        level = logging.getLevelName(level.upper())
        name = log_conf.get('name', '')
        if not name:
            name = str(k)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        handlers_conf = log_conf.get('handlers')
        if not handlers_conf:
            h = create_std_handler('', {})
            logger.addHandler(h)
        else:
            for hc in handlers_conf:
                if 'type' not in hc:
                    raise exception.ConfigParseException()
                if hc.get('type') not in HANDLER_CREATOR.keys():
                    raise exception.ConfigParseException()
                t = hc.get('type')
                h = HANDLER_CREATOR.get(t)(k, hc)
                logger.addHandler(h)
        _LOGGER_MAP[str(k)] = logger
    return _LOGGER_MAP[logger_key]


def get_logger(logger_key='common'):
    """
    根据key的不同获取不同的日志
    :param logger_key:
    :return:
    """
    global _LOGGER_MAP
    if logger_key not in _LOGGER_MAP.keys():
        raise exception.InvalidLoggerKeyException()
    return _LOGGER_MAP[logger_key]


def generate_sample_config(filename):
    """
    复制一份示例配置文件
    :param filename: 目标文件路径
    :return:
    """
    with open(filename, 'w', encoding='utf8') as f:
        toml.dump(config.SAMPLE_CONFIG, f)
