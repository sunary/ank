__author__ = 'sunary'


import time
from apps._app import App
from datetime import datetime, timedelta


class ScheduleApp(App):
    '''
    schedule process
    '''

    def __init__(self, crontab_time, start_now=False):
        super(ScheduleApp, self).__init__()
        self.crontab_reader = CrontabTimeReader(crontab_time)
        self.start_now = start_now

    def run(self, process=None):
        super(ScheduleApp, self).run(process)

        if self.start_now:
            self._run()

        while True:
            time.sleep(60)

            next_time = self.crontab_reader.get_next_time()
            self.logger.info('sleep to %s' % next_time)

            second_to_wait = (next_time - datetime.utcnow()).total_seconds()
            time.sleep(second_to_wait)
            self.process()

    def _run(self):

        raise NotImplementedError

    def process(self, messages=None):

        return messages


class CrontabTimeReader():

    def __init__(self, time_str):
        time_str = time_str.split(' ')

        assert len(time_str) == 5, 'Cronjob time need 5 fields'

        self.minute, self.hour, self.day, self.month, self.day_of_week =\
            self.normalized_value(time_str[0]), self.normalized_value(time_str[1]), self.normalized_value(time_str[2]), self.normalized_value(time_str[3]), self.normalized_value(time_str[4])

        print self.minute, self.hour, self.day, self.month, self.day_of_week

    def normalized_value(self, value):
        ret_value = []
        if '-' in value:
            value = value.split('-')
            for n in range(int(value[0]), int(value[1]) + 1):
                ret_value.append(n)

        elif ',' in value:
            value = value.split(',')
            for n in value:
                ret_value.append(int(n))

        elif value == '*':
            return '*'
        else:
            return [int(value)]

        return ret_value

    def get_next_time(self):
        now = datetime.utcnow()
        valid_hours = range(24) if self.hour == '*' else self.hour
        valid_minutes = range(60) if self.minute == '*' else self.minute

        combine_time = []
        for h in valid_hours:
            for m in valid_minutes:
                combine_time.append([h, m])

        combine_time.sort()
        combine_time_now = [now.hour, now.minute]

        if self.day != '*':
            if (self.month == '*' or now.month in self.month) and now.day in self.day:
                for t in combine_time:
                    if t > combine_time_now:
                        return now.replace(hour=t[0], minute=t[1])
        elif self.day_of_week != '*':
            if now.weekday() in self.day_of_week:
                for t in combine_time:
                    if t > combine_time_now:
                        return now.replace(hour=t[0], minute=t[1])
        else:
            for t in combine_time:
                if t > combine_time_now:
                    return now.replace(hour=t[0], minute=t[1])

        if self.day != '*':
            combine_day = []
            valid_month = range(1, 13) if self.month == '*' else self.month
            for m in valid_month:
                for d in self.day:
                    combine_day.append([m, d])

            combine_day.sort()
            combine_day_now = [now.month, now.day]
            for d in combine_day:
                if d > combine_day_now:
                    return now.replace(month=d[0], day=d[1], hour=combine_time[0][0], minute=combine_time[0][1])

            return now.replace(year=now.year + 1, month=combine_day[0][0], day=combine_day[0][1], hour=combine_time[0][0], minute=combine_time[0][1])
        elif self.day_of_week != '*':
            num_day = min(map(lambda x: x - now.weekday() if x > now.weekday() else x + 7 - now.weekday(), self.day_of_week))
            return (now + timedelta(hours=24 * num_day)).replace(hour=combine_time[0][0], minute=combine_time[0][1])
        else:
            return (now + timedelta(hours=24)).replace(hour=combine_time[0][0], minute=combine_time[0][1])


if __name__ == '__main__':
    timer_reader = CrontabTimeReader('55 23 2,4,6 3 *')
    print timer_reader.get_next_time()
    timer_reader = CrontabTimeReader('0 2,3 * * 0-5')
    print timer_reader.get_next_time()