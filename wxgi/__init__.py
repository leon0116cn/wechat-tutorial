from flask import Flask
from flask import request
from wxgi import settings
from wxgi.utils import check_signature
from wxgi.utils import parse_xml
from wxgi import models


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    
    @app.route('/')
    def index():
        return 'hello world.'

    @app.route('/wx', methods=['POST', 'GET'])
    def handle():
        if request.method == 'GET':
            echostr = request.args.get('echostr')
            signature = request.args.get('signature')
            timestamp = request.args.get('timestamp')
            nonce = request.args.get('nonce')
            token = settings.WECHAT_APP_TOKEN

            if not check_signature(token, timestamp, nonce, signature):
                return ''

            return echostr

        elif request.method == 'POST':
            web_data = request.data.decode('utf-8')
            print('handle/POST fun: web_data is:\n', web_data)
            
            rec_msg = parse_xml(web_data)

            if isinstance(rec_msg, models.WechatMsg):
                to_user = rec_msg.from_user
                from_user = rec_msg.to_user

                if rec_msg.msg_type == 'text':
                    content = rec_msg.content
                    reply_msg = models.TextReplyMsg(to_user, from_user, content) 
                    return reply_msg.reply()
                elif rec_msg.msg_type == 'image':
                    media_id = rec_msg.media_id
                    reply_msg = models.ImageReplyMsg(to_user, from_user, media_id)
                    return reply_msg.reply()
                else:
                    reply_msg = models.ReplyMsg()
                    return reply_msg.reply()
            else:
                print('暂不处理...')
                return models.ReplyMsg().reply()

    @app.route('/token')
    def access_token():
        access_token = models.WechatAccessToken()
        return access_token.get_access_token()

    return app