# -*- coding: utf-8 -*-
__author__ = 'sunary'


def init_logger(name, log_level=None, log_file='log.log'):
    import logging
    import logging.handlers

    logger = logging.getLogger(name)

    if log_level:
        logger.setLevel(log_level)
    else:
        logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')

    if log_file:
        fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=2 * 1024 * 1024, backupCount=3)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    else:
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    return logger


if __name__ == '__main__':
    import logging
    logger = init_logger('test', logging.INFO, None, 'v2nhat@gmail.com')
    logger.info('info')
    logger.debug('debug')
    logger.warning('warning')
    logger.error('error')