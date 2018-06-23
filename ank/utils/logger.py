# -*- coding: utf-8 -*-
__author__ = 'sunary'


import os
import logging
import logging.handlers


def init_logger(name, log_level=None, log_file=None):
    _logger = logging.getLogger(name)

    if log_level:
        _logger.setLevel(log_level)
    else:
        _logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')

    if not log_file:
        log_file = '{}.log'.format(name)

    if log_file:
        if not os.path.exists(log_file):
            with open(log_file, 'w') as of:
                of.write('')

        fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=2 * 1024*1024, backupCount=3)
        fh.setFormatter(formatter)
        _logger.addHandler(fh)
    # else:
    #     sh = logging.StreamHandler()
    #     sh.setFormatter(formatter)
    #     logger.addHandler(sh)

    return _logger


if __name__ == '__main__':
    logger = init_logger('test', logging.INFO)
    logger.info('info')
    logger.debug('debug')
    logger.warning('warning')
    logger.error('error')
