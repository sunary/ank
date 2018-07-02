__author__ = 'sunary'


from ank.apps.schedule_app import ScheduleApp
from datetime import datetime


class ScheduleExample(ScheduleApp):

    def init_app(self, crontab_time='', start_now=False):
        super(ScheduleExample, self).init_app(crontab_time, start_now)

    def start(self):
        pass

    def process(self, messages=None):
        print('Now is {}'.format(datetime.now()))