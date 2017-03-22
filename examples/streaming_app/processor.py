# -*- coding: utf-8 -*-
__author__ = 'sunary'


from base_apps.pipe_app import PipeApp
try:
    import tweepy
    from tweepy.streaming import StreamListener, json
except ImportError:
    raise ImportError('No module named tweepy')


class TwitterSpout(PipeApp):

    def init_app(self, key):
        self.key = key

        self.listener = StreamListener()
        self.listener.on_data = self.on_messages_received
        self.listener.on_error = self.on_error

    def start(self):
        auth = tweepy.OAuthHandler(self.key['consumer_key'], self.key['consumer_secret'])
        auth.set_access_token(self.key['access_token'], self.key['access_token_secret'])

        self.stream_engine = tweepy.Stream(auth, self.listener)
        self.filter()

    def on_messages_received(self, messages):
        messages = json.loads(messages)
        self.chain_process(messages)

        return True

    def on_error(self, status_code):
        if status_code == 88:
            self.logger.info('code 88, Rate limit exceeded')
            self.get_engine()
        elif status_code == 401:
            self.logger.info('code 401, Unauthorized')
            if self.twitter_key.report():
                self.get_engine()
        else:
            self.logger.info('code %s' % status_code)

    def filter(self):
        '''
        Filter tweet
        '''
        user_ids = ['111489227']
        self.stream_engine.filter(follow=user_ids)

    def user_stream(self):
        '''
        User stream
        '''
        self.stream_engine.userstream()

    def process(self, messages=None):

        return messages