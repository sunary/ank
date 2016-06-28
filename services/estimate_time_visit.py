__author__ = 'sunary'


from datetime import datetime, timedelta


class BehaviorEstimate():
    '''
    Estimate next time visit page in REST crawler
    '''
    LENGTH_HISTOGRAM = 50
    CUMULATIVE_DAYS_VISIT = 14
    PERCENT_SUBTRACT = 2.0

    def __init__(self, min_times=0.2, max_times=10.0, scale_times=3.0):
        self.MIN_TIMES_VISIT_PER_DAY = min_times
        self.MAX_TIMES_VISIT_PER_DAY = max_times
        self.SCALE_TIMES_VISIT = scale_times

        self.histogram = [100.0/self.LENGTH_HISTOGRAM] * self.LENGTH_HISTOGRAM
        self.average_times_visit_per_day = self.SCALE_TIMES_VISIT
        self.activated_date = None
        self.range_day = 0
        self.date_visit = [{'date': datetime(2015, 1, 1), 'times_visit': 0} for _ in range(self.CUMULATIVE_DAYS_VISIT + 6)]
        self.time_msg = None
        self.date_has_message = None

    def set(self, data):
        '''
        Set estimate data

        Args:
            data (dict): {'histogram': , 'activated_date': , 'date_visit': }
        '''
        self.histogram = data.get('histogram') if data.get('histogram') else self.histogram
        self.activated_date = data.get('activated_date') if data.get('activated_date') else self.activated_date
        self.date_visit = data.get('date_visit') if data.get('date_visit') else self.date_visit

    def get(self):
        data_update = {}
        data_update['histogram'] = self.histogram
        data_update['activated_date'] = self.activated_date
        data_update['date_visit'] = self.date_visit
        data_update['next_crawl_time'] = self._next_time_visit()

        return data_update

    def has_messages(self, time_msg):
        '''
        Change status if page have a message

        Args:
            time_msg: time message was created
        '''

        self.time_msg = time_msg
        self.date_has_message = self.time_msg.replace(hour= 0, minute= 0, second= 0, microsecond= 0)

        if not self.activated_date or self.activated_date > self.time_msg:
            self.activated_date = self.date_has_message
        elif self.range_day < self.CUMULATIVE_DAYS_VISIT:
            self.range_day = (self.time_msg - self.activated_date).days
            self.range_day = self.CUMULATIVE_DAYS_VISIT if self.range_day > self.CUMULATIVE_DAYS_VISIT else self.range_day

        for i in range(len(self.date_visit)):
            if self.date_visit[i]['date'] == self.date_has_message:
                self.date_visit[i]['times_visit'] += 1
                break
        else:
            for i in range(len(self.date_visit)):
                if self.date_visit[i]['date'] < (self.date_has_message - timedelta(days=self.CUMULATIVE_DAYS_VISIT)):
                    self.date_visit[i]['date'] = self.date_has_message
                    self.date_visit[i]['times_visit'] = 1
                    break
        self._update()

    def _update(self):
        total_visit = 0
        for i in range(len(self.date_visit)):
            if self.date_visit[i]['date'] < self.date_has_message and self.date_visit[i]['date'] >= (self.date_has_message - timedelta(days=self.CUMULATIVE_DAYS_VISIT)):
                total_visit += self.date_visit[i]['times_visit']

        if self.range_day == 0:
            for i in range(len(self.date_visit)):
                if self.date_visit[i]['date'] == self.date_has_message:
                    self.average_times_visit_per_day = max(self.date_visit[i]['times_visit'], self.SCALE_TIMES_VISIT)
                    break
        else:
            self.average_times_visit_per_day = total_visit*self.SCALE_TIMES_VISIT/self.range_day

        self.average_times_visit_per_day = self.MAX_TIMES_VISIT_PER_DAY if (self.average_times_visit_per_day > self.MAX_TIMES_VISIT_PER_DAY)\
            else self.average_times_visit_per_day
        self.average_times_visit_per_day = self.MIN_TIMES_VISIT_PER_DAY if (self.average_times_visit_per_day < self.MIN_TIMES_VISIT_PER_DAY)\
            else self.average_times_visit_per_day

        for i in range(len(self.histogram)):
            self.histogram[i] -= self.histogram[i]*self.PERCENT_SUBTRACT/100

        self.histogram[self._order_histogram()] += self.PERCENT_SUBTRACT

    def _next_time_visit(self):
        '''
        Get next time visit page by status

        Returns:
            (datetime) next time visit
        '''
        num_unit = 0
        order_histogram = self._order_histogram()
        probability_visit = 0
        while probability_visit < 1:
            num_unit += 1
            probability_visit += self.histogram[order_histogram]*self.average_times_visit_per_day/100
            order_histogram = (order_histogram + 1) % self.LENGTH_HISTOGRAM

        return datetime.today() + timedelta(minutes=num_unit*24*60/self.LENGTH_HISTOGRAM)

    def _order_histogram(self):
        '''
        get order histogram to next time visit

        Returns:
            int: order of histogram
        '''
        if not self.time_msg:
            self.time_msg = datetime.utcnow()
        minutes = self.time_msg.hour*60 + self.time_msg.minute
        return minutes*self.LENGTH_HISTOGRAM/(24*60)

    def _change_len_histogram(self, new_len_histogram):
        new_histogram = [0]*new_len_histogram
        for i in range(len(new_histogram)):
            new_histogram[i] = self.histogram[int(round(i*self.LENGTH_HISTOGRAM*1.0/new_len_histogram))]

        sum_new_histogram = 0
        for i in range(len(new_histogram)):
            sum_new_histogram += new_histogram[i]

        for i in range(len(new_histogram)):
            new_histogram[i] *= 100.0/sum_new_histogram

        self.histogram = new_histogram
        self.LENGTH_HISTOGRAM = new_len_histogram

    @staticmethod
    def datetime_from_string(str_date, date_format='iso'):
        '''
        convert string to datetime

        Examples:
            >>> BehaviorEstimate.datetime_from_string('2015-07-17 06:07:22.375866')
            datetime.datetime(2015, 07, 17, 06, 07, 22)
            >>> BehaviorEstimate.datetime_from_string('Wed Oct 07 15:49:44 +0000 2009')
            datetime.datetime(2009, 10, 07, 15, 49, 44)
        '''
        if date_format == 'iso':
            return datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
        elif date_format == 'mongo':
            str_date = str_date.split('.')[0]
            return datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
        elif date_format == 'twitter':
            str_date = str_date.split(' ')
            del str_date[4]
            str_date = ' '.join(str_date)
            return datetime.strptime(str_date, '%a %b %d %H:%M:%S %Y')

        return None


if __name__ == '__main__':
    actor = BehaviorEstimate()
    actor.set({})
    actor.has_messages(datetime(2015, 6, 3))
    print actor.get()['next_crawl_time']