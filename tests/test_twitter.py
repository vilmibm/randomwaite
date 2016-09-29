from unittest import TestCase
from unittest.mock import patch

from tweepy import TweepError

import randomwaite.twitter as rt
from randomwaite.errors import TwitterMessedUpException
from randomwaite.twitter import twitter_retry

class TestTwitterRetrier(TestCase):
    def test_successful_call(self):
        def fake_twitter_call(x, y):
            return x + y
        under_test = twitter_retry(fake_twitter_call)
        self.assertEqual(3, under_test(1,2))

    @patch('randomwaite.twitter.logger')
    def test_handles_one_error(self, logger_mock):
        called = False
        def fake_twitter_call(x, y):
            nonlocal called
            if not called:
                called = True
                raise TweepError('foobar')
            return x + y
        under_test = twitter_retry(fake_twitter_call)

        result = under_test(660,6)
        self.assertEqual(1, len(logger_mock.exception.call_args_list))
        self.assertTrue(called)
        self.assertEqual(666, result)

    @patch('randomwaite.twitter.sleep')
    @patch('randomwaite.twitter.logger')
    def test_stops_trying(self, logger_mock, sleep_mock):
        def fake_twitter_call(x, y):
            raise TweepError('foobar')
        under_test = twitter_retry(fake_twitter_call)
        with self.assertRaises(TwitterMessedUpException):
            under_test(1,2)
        self.assertEqual(rt.MAX_RETRIES, len(logger_mock.exception.call_args_list))
        self.assertTrue(sleep_mock.called)

    @patch('randomwaite.twitter.sleep')
    @patch('randomwaite.twitter.logger')
    def test_none_result(self, logger_mock, sleep_mock):
        def fake_twitter_call(x,y):
            return None
        under_test = twitter_retry(fake_twitter_call)
        result = under_test(1,2)
        self.assertEqual(result, None)
        self.assertFalse(sleep_mock.called)
