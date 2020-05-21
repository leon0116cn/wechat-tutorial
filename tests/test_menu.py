import unittest
import json
from wxgi.models import WechatAccessToken
from wxgi.menu import WechatMenu
from wxgi import settings


class TestMenu(unittest.TestCase):
    def setUp(self):
        self._access_token = WechatAccessToken().get_access_token()
        self._menu = WechatMenu()

    def test_create_menu(self):
        post_data = None
        with open(settings.WECHAT_MENU_PATH, encoding='utf-8') as f:
            post_data = json.load(f)

        self.assertTrue(self._menu.create(post_data, self._access_token))

    def test_current_menu(self):
        current_menu = self._menu.get_current_menu(self._access_token)
        print(current_menu)
        self.assertIsNotNone(current_menu)

    def test_delete(self):
        self.assertTrue(self._menu.delete(self._access_token))
