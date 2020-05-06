import unittest
from wxgi.models import WechatAccessToken
from wxgi.utils import callback_ip, api_domain_ip, create_menu, delete_menu, current_menu


class Test_Utils(unittest.TestCase):
    def setUp(self):
        self.access_token = WechatAccessToken().get_access_token()

    def test_callback_ip(self):
        ips = callback_ip(self.access_token)
        print('Wechat callback ip:\n{}'.format(ips))
        self.assertIsNotNone(ips)
        
    def test_api_domain_ip(self):
        ips = api_domain_ip(self.access_token)
        print('Wechat api domain ip:\n{}'.format(ips))
        self.assertIsNotNone(ips)
    
    def test_create_menu(self):
        self.assertTrue(create_menu(self.access_token, 'unittestcases/menu.json'))

    def test_current_menu(self):
        menu = current_menu(self.access_token)
        print('Wechat current menu:\n{}'.format(menu))
        self.assertIsNotNone(menu)

    def test_delete_menu(self):
        self.assertTrue(delete_menu(self.access_token))