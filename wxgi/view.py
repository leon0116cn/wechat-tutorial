from flask import request
from wxgi import app, settings, receive, reply
from wxgi.basic import check_signature, WechatAccessToken


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
        open_id = request.args.get('openid')
        print('handle/POST Openid:{}'.format(open_id))
        print('Post data:\n', web_data)

        rec_msg = receive.parse_xml(web_data)

        if isinstance(rec_msg, receive.WechatMsg):
            to_user = rec_msg.from_user
            from_user = rec_msg.to_user

            if rec_msg.msg_type == 'text':
                content = rec_msg.content
                reply_msg = reply.TextReplyMsg(to_user, from_user, content) 
                return reply_msg.reply()
            elif rec_msg.msg_type == 'image':
                media_id = rec_msg.media_id
                reply_msg = reply.ImageReplyMsg(to_user, from_user, media_id)
                return reply_msg.reply()
            elif rec_msg.msg_type == 'location':
                reply_msg = reply.TextReplyMsg(to_user, from_user, str(rec_msg))
                return reply_msg.reply()
            else:
                reply_msg = reply.ReplyMsg()
                return reply_msg.reply()
            
        if isinstance(rec_msg, receive.WechatEventMsg):
            to_user = rec_msg.from_user
            from_user = rec_msg.to_user
                
            if rec_msg.msg_event == 'CLICK':
                event_key = rec_msg.event_key
                if event_key == 'mpGuide':
                    content = '{}功能编写中，尚未完成...'.format(event_key)
                    reply_msg = reply.TextReplyMsg(to_user, from_user, content)
                    return reply_msg.reply()
            elif rec_msg.msg_event == 'subscribe':
                content = '欢迎订阅公众号...'
                reply_msg = reply.TextReplyMsg(to_user, from_user, content)
                return reply_msg.reply()
            elif rec_msg.msg_event == 'unsubscribe':
                content = '欢迎再次订阅公众号...'
                reply_msg = reply.TextReplyMsg(to_user, from_user, content)
                return reply_msg.reply()
            elif rec_msg.msg_event == 'VIEW':
                content = str(rec_msg)
                print('content:{}'.format(content))
                return reply.ReplyMsg().reply()
                    
        print('暂不处理...')
        return reply.ReplyMsg().reply()


@app.route('/wx/token')
def access_token():
    access_token = basic.WechatAccessToken()
    return access_token.get_access_token()