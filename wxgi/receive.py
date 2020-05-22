import xml.etree.ElementTree as ET


def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    
    xml_data = ET.fromstring(web_data)
    msg_type = xml_data.find('MsgType').text
    if msg_type == 'event':
        msg_event = xml_data.find('Event').text       
        if msg_event == 'CLICK':
            return ClickWechatEventMsg(xml_data)
        elif msg_event in ['subscribe', 'unsubscribe']:
            return SubscribeWechatEventMsg(xml_data)
        elif msg_event == 'VIEW':
            return ViewWechatEventMsg(xml_data)
        else:
            return WechatEventMsg(xml_data)

    elif msg_type == 'text':
        return TextWechatMsg(xml_data)
    
    elif msg_type == 'image':
        return ImageWechatMsg(xml_data)

    elif msg_type == 'location':
        return LocationWechatMsg(xml_data)
    else:
        return WechatMsg(xml_data)


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


class LocationWechatMsg(WechatMsg):
    def __init__(self, xml_data):
        super().__init__(xml_data)
        self.location_x = xml_data.find('Location_X').text
        self.location_y = xml_data.find('Location_Y').text
        self.scale = xml_data.find('Scale').text
        self.label = xml_data.find('Label').text


class WechatEventMsg:
    def __init__(self, xml_data):
        self.to_user = xml_data.find('ToUserName').text
        self.from_user = xml_data.find('FromUserName').text
        self.create_time = xml_data.find('CreateTime').text
        self.msg_type = xml_data.find('MsgType').text
        self.msg_event = xml_data.find('Event').text


class ClickWechatEventMsg(WechatEventMsg):
    def __init__(self, xml_data):
        super().__init__(xml_data)
        self.event_key = xml_data.find('EventKey').text


class SubscribeWechatEventMsg(WechatEventMsg):
    def __init__(self, xml_data):
        super().__init__(xml_data)


class ViewWechatEventMsg(WechatEventMsg):
    def __init__(self, xml_data):
        super().__init__(xml_data)
        self.event_key = xml_data.find('EventKey').text
        self.menu_id = xml_data.find('MenuId').text
