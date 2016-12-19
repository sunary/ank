__author__ = 'sunary'


from apps.schedule_app import ScheduleApp
from datetime import datetime


class ScheduleExample(ScheduleApp):

    def __init__(self, crontab_time, start_now=False, **kwargs):
        super(ScheduleExample, self).__init__(crontab_time, start_now)

    def run(self, process=None):
        super(ScheduleApp, self).run(process)

    def process(self, messages=None):
        print('Now is {}'.format(datetime.now()))