import unittest
from wxgi.models import WechatMessageEven
from wxgi.models import WechatAccessToken


WECHAT_TEXT_MSG = '''
<xml>
  <ToUserName><![CDATA[toUser]]></ToUserName>
  <FromUserName><![CDATA[fromUser]]></FromUserName>
  <CreateTime>1348831860</CreateTime>
  <MsgType><![CDATA[text]]></MsgType>
  <Content><![CDATA[this is a test]]></Content>
  <MsgId>1234567890123456</MsgId>
</xml>
'''
WECHAT_PIC_MSG = '''
<xml>
  <ToUserName><![CDATA[toUser]]></ToUserName>
  <FromUserName><![CDATA[fromUser]]></FromUserName>
  <CreateTime>1348831860</CreateTime>
  <MsgType><![CDATA[image]]></MsgType>
  <PicUrl><![CDATA[this is a url]]></PicUrl>
  <MediaId><![CDATA[media_id]]></MediaId>
  <MsgId>1234567890123456</MsgId>
</xml>
'''
WECHAT_SUBSCRIBE_EVENT = '''
<xml>
  <ToUserName><![CDATA[toUser]]></ToUserName>
  <FromUserName><![CDATA[FromUser]]></FromUserName>
  <CreateTime>123456789</CreateTime>
  <MsgType><![CDATA[event]]></MsgType>
  <Event><![CDATA[subscribe]]></Event>
</xml>
'''


class Test_Models(unittest.TestCase):
    def setUp(self):
        self.access_token = WechatAccessToken().get_access_token()

    def test_get_access_token(self):
        print('Access token :{}'.format(self.access_token))
        self.assertIsNotNone(self.access_token)

    def test_wechat_text_msg(self):
        text_msg = WechatMessageEven(WECHAT_TEXT_MSG)
        self.assertEqual(text_msg.get('MsgType'), 'text')
        print(text_msg)

    def test_wechat_pic_msg(self):
        pic_msg = WechatMessageEven(WECHAT_PIC_MSG)
        self.assertEqual(pic_msg.get('MsgType'), 'image')
        print(pic_msg)

    def test_wechat_subscribe_event(self):
        event_msg = WechatMessageEven(WECHAT_SUBSCRIBE_EVENT)
        self.assertEqual(event_msg.get('MsgType'), 'event')
        print(event_msg)
        
