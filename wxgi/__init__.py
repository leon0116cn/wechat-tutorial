from flask import Flask
from wxgi import settings
from wxgi.utils import check_signature
from wxgi.models import WechatAccessToken


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    wechat_access_token = WechatAccessToken().get_access_token()

    @app.route('/')
    def hello():
        return 'hello world.'

    @app.route('/weixin_init')
    def weixin_init():
        echostr = request.args.get('echostr')
        signature = params.get('signature')
        timestamp = params.get('timestamp')
        nonce = params.get('nonce')
        token = settings.WECHAT_APP_TOKEN

        if not check_signature(token, timestamp, nonce, signature):
            return ''
        
        return echostr

    @app.route('/weixin_accesstoken')
    def weixin_accesstoken():
        return wechat_access_token

    return app