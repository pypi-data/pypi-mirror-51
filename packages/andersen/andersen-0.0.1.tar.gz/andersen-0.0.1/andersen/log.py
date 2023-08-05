import os

from . import logger_helper as lh

logger = None
inited = False


def init(conf=None, default_logger='common'):
    """
    初始化
    :param conf 这个参数
    :param default_logger 默认的日志对象的key
    :return:
    """
    global logger, inited
    if inited:
        return
    if conf is None:
        conf = os.environ.get('ANDERSEN_CONFIG', None)
    lh.load_config(conf)
    lh.init_logger()
    logger = lh.get_logger(default_logger)
    inited = True


def get_logger(key='common'):
    return lh.get_logger(key)


def generate_sample_config(filename):
    """
    生成示例配置文件
    :param filename:
    :return:
    """
    lh.generate_sample_config(filename)


def _get_param(kwargs):
    global logger
    list_sep = ', '
    dict_sep = '\n'
    para_sep = '\n'
    if 'sep' in kwargs:
        list_sep = kwargs['sep']
        dict_sep = kwargs['sep']
        para_sep = kwargs['sep']
        del kwargs['sep']
    if 'list_sep' in kwargs:
        list_sep = kwargs['list_sep']
        del kwargs['list_sep']
    if 'dict_sep' in kwargs:
        dict_sep = kwargs['dict_sep']
        del kwargs['dict_sep']
    if 'para_sep' in kwargs:
        para_sep = kwargs['para_sep']
        del kwargs['para_sep']
    local_log = logger
    if 'logger' in kwargs:
        local_log = lh.get_logger(kwargs['logger'])
        del kwargs['logger']
    return local_log, list_sep, dict_sep, para_sep


def _log_args(args, list_sep):
    if not args:
        return ''
    args = [str(arg) for arg in args]
    return list_sep.join(args)


def _log_kwargs(kwargs, dict_sep):
    if not kwargs:
        return ''
    out_str = []
    for k, v in kwargs.items():
        out_str.append(f'{str(k)}={str(v)}')
    return dict_sep.join(out_str)


def debug(*args, **kwargs):
    local_log, list_sep, dict_sep, para_sep = _get_param(kwargs)
    out_str1 = _log_args(args, list_sep)
    out_str2 = _log_kwargs(kwargs, dict_sep)
    if out_str1 and out_str2:
        out_str = para_sep.join([out_str1, out_str2])
    elif out_str1:
        out_str = out_str1
    elif out_str2:
        out_str = out_str2
    else:
        out_str = ''
    local_log.debug(out_str)


def info(*args, **kwargs):
    local_log, list_sep, dict_sep, para_sep = _get_param(kwargs)
    out_str1 = _log_args(args, list_sep)
    out_str2 = _log_kwargs(kwargs, dict_sep)
    if out_str1 and out_str2:
        out_str = para_sep.join([out_str1, out_str2])
    elif out_str1:
        out_str = out_str1
    elif out_str2:
        out_str = out_str2
    else:
        out_str = ''
    local_log.info(out_str)


def warn(*args, **kwargs):
    local_log, list_sep, dict_sep, para_sep = _get_param(kwargs)
    out_str1 = _log_args(args, list_sep)
    out_str2 = _log_kwargs(kwargs, dict_sep)
    if out_str1 and out_str2:
        out_str = para_sep.join([out_str1, out_str2])
    elif out_str1:
        out_str = out_str1
    elif out_str2:
        out_str = out_str2
    else:
        out_str = ''
    local_log.warn(out_str)


def error(*args, **kwargs):
    local_log, list_sep, dict_sep, para_sep = _get_param(kwargs)
    out_str1 = _log_args(args, list_sep)
    out_str2 = _log_kwargs(kwargs, dict_sep)
    if out_str1 and out_str2:
        out_str = para_sep.join([out_str1, out_str2])
    elif out_str1:
        out_str = out_str1
    elif out_str2:
        out_str = out_str2
    else:
        out_str = ''
    local_log.error(out_str)


init()
inited = False
