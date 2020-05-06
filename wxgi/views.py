from flask import Blueprint
from flask import request
from wxgi import settings
from wxgi.utils import check_signature


bp = Blueprint('wechat', __name__, url_prefix='/wx')


@bp.route('/')
def hello():
    return 'Hello Blueprint /wechat'


@bp.route('/check_signature')
def weixin_init():
    echostr = request.args.get('echostr')
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    token = settings.WECHAT_APP_TOKEN

    if not check_signature(token, timestamp, nonce, signature):
        return ''
        
    return echostr