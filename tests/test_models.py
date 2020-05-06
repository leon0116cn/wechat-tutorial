import unittest
from wxgi.models import WechatAccessToken


class Test_Models(unittest.TestCase):
    def setUp(self):
        self.access_token = WechatAccessToken().get_access_token()

    def test_get_access_token(self):
        print('Access token :{}'.format(self.access_token))
        self.assertIsNotNone(self.access_token)
