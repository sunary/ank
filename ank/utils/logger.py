# -*- coding: utf-8 -*-
__author__ = 'sunary'


import os
import logging
import logging.handlers


LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s: %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def _get_log_level():
    """Resolve log level from ANK_LOG_LEVEL env var."""
    level = os.environ.get('ANK_LOG_LEVEL', '').upper()
    return getattr(logging, level, None)


def init_logger(name, log_level=None, log_file=None):
    """
    Get or create a logger with optional console and file handlers.

    Args:
        name: Logger name (e.g. class name)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR). Falls back to
                  ANK_LOG_LEVEL env var, then INFO.
        log_file: Path to log file. If True, uses '{name}.log'. If False, no file.
                  Default True.

    Returns:
        logging.Logger
    """
    _logger = logging.getLogger(name)

    level = log_level or _get_log_level() or logging.INFO
    _logger.setLevel(level)

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # Avoid duplicate handlers when same logger is reused
    if _logger.handlers:
        return _logger

    # Console output (stdout)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    _logger.addHandler(sh)

    # Optional file output
    if log_file is None:
        log_file = '{}.log'.format(name)
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        fh = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=2 * 1024 * 1024,
            backupCount=3,
            encoding='utf-8',
        )
        fh.setFormatter(formatter)
        _logger.addHandler(fh)

    return _logger


if __name__ == '__main__':
    logger = init_logger('test', logging.INFO)
    logger.info('info')
    logger.debug('debug')
    logger.warning('warning')
    logger.error('error')
