__author__ = 'sunary'


import time
from ank.base_apps.pipe_app import PipeApp
from datetime import datetime
from ank.utils.crontab_time import CrontabTimeReader


class ScheduleApp(PipeApp):
    """
    Schedule process using crontab time format
    """

    def init_app(self, crontab_time='', start_now=False):
        """
        Args:
            crontab_time (string): cronjob time format
            start_now (bool): is start after init
        """
        self.crontab_reader = CrontabTimeReader(crontab_time)
        self.start_now = start_now
        self.logger.info('crontad time after extract: %s', self.crontab_reader)

    def start(self):
        if self.start_now:
            self.process()
            time.sleep(60)

        while True:
            next_time = self.crontab_reader.get_next_time()
            self.logger.info('sleep to %s' % next_time)

            second_to_wait = (next_time - datetime.utcnow()).total_seconds()
            time.sleep(second_to_wait)
            self.process()

    def process(self, message=None):

        return message
