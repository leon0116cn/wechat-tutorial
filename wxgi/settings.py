import os


WECHAT_APP_ID = os.environ.get('WECHAT_APP_ID')
WECHAT_APP_SECRET = os.environ.get('WECHAT_APP_SECRET')
WECHAT_APP_TOKEN = os.environ.get('WECHAT_APP_TOKEN')


REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = int(os.environ.get('REDIS_PORT'))
REDIS_DB = int(os.environ.get('REDIS_DB'))


REDIS_ACCESSTOKEN_KEY = 'wx:accesstoken'
WECHAT_ACCESSTOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token'
WECHAT_CALLBACK_IP_URL = 'https://api.weixin.qq.com/cgi-bin/getcallbackip'
WECHAT_API_DOMAIN_IP_URL = 'https://api.weixin.qq.com/cgi-bin/get_api_domain_ip'
WECHAT_CREATE_MENU_URL = 'https://api.weixin.qq.com/cgi-bin/menu/create'
WECHAT_DELETE_MENU_URL = 'https://api.weixin.qq.com/cgi-bin/menu/delete'
WECHAT_CURRENT_MENU_URL = 'https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info'