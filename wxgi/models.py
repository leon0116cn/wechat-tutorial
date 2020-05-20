from datetime import datetime
import xml.etree.ElementTree as ET
import requests
import redis
from wxgi import settings


class WechatMsg:
    def __init__(self, xml_data):
        self.to_user = xml_data.find('ToUserName').text
        self.from_user = xml_data.find('FromUserName').text
        self.create_time = xml_data.find('CreateTime').text
        self.msg_type = xml_data.find('MsgType').text
        self.msg_id = xml_data.find('MsgId').text


class TextWechatMsg(WechatMsg):
    def __init__(self, xml_data):
        super().__init__(xml_data)
        self.content = xml_data.find('Content').text


class ImageWechatMsg(WechatMsg):
    def __init__(self, xml_data):
        super().__init__(xml_data)
        self.pic_url = xml_data.find('PicUrl').text
        self.media_id = xml_data.find('MediaId').text


class ReplyMsg:
    def __init__(self):
        pass

    def reply(self):
        return 'success'


class TextReplyMsg(ReplyMsg):
    def __init__(self, to_user, from_user, content):
        self.__dict = {}
        self.__dict['ToUserName'] = to_user
        self.__dict['FromUserName'] = from_user
        self.__dict['CreateTime'] = int(datetime.now().timestamp())
        self.__dict['Content'] = content

    def reply(self):
        xml_form = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{Content}]]></Content>
            </xml>
            """
        return xml_form.format(**self.__dict)


class ImageReplyMsg(ReplyMsg):
    def __init__(self, to_user, from_user, media_id):
        self.__dict = {}
        self.__dict['ToUserName'] = to_user
        self.__dict['FromUserName'] = from_user
        self.__dict['CreateTime'] = int(datetime.now().timestamp())
        self.__dict['MediaId'] = media_id

    def reply(self):
        xml_form = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                <MediaId><![CDATA[{MediaId}]]></MediaId>
                </Image>
            </xml>
            """
        
        return xml_form.format(**self.__dict)


class WechatAccessToken:
    def __init__(self):
        self.rds = redis.Redis(
            host=settings.REDIS_HOST, 
            port=settings.REDIS_PORT, 
            db=settings.REDIS_DB
            )

    def _refresh_access_token(self):
        try:
            r = requests.get(
                settings.WECHAT_ACCESSTOKEN_URL,
                params=settings.WECHAT_ACCESSTOKEN_PAYLOAD,
                timeout=10
                )
            r.raise_for_status()
            access_token = r.json()
        except requests.HTTPError as e:
            print('Wechat connection error!')
            print(e)
        except ValueError as e:
            print('No json object return!')
            print(e)

        if 'errcode' in access_token:
            print('Wechat return error!')
            print(access_token.get('errcode'), access_token.get('errmsg'))
            return None
    
        return access_token

    def _cache_access_token(self, token, ex):
        self.rds.set(settings.REDIS_ACCESSTOKEN_KEY, token, ex=ex)

    def _query_access_token(self):
        access_token = self.rds.get(settings.REDIS_ACCESSTOKEN_KEY)
        if access_token:
            return access_token.decode('utf-8')
            
    def get_access_token(self):
        access_token = self._query_access_token()

        if access_token is None:
            new_access_token = self._refresh_access_token()

            if new_access_token:
                access_token = new_access_token.get('access_token')
                expire_in = new_access_token.get('expires_in')
                self._cache_access_token(access_token, expire_in)
        
        return access_token


class WechatMessageEven(dict):
    def __init__(self, message):
        self.msg = {}
        
        xml_msg = ET.fromstring(message)
        for ele in xml_msg:
            self.msg[ele.tag] = ele.text
        
        self.update(self.msg)
   
        