from datetime import datetime


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