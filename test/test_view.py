import unittest
from wxgi import app


class ViewTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_app_exist(self):
        self.assertIsNotNone(app)

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('hello world.', data)

    def test_get_handle(self):
        response = self.client.get('/wx?signature=44232ff8ec5a4bc7ca6fff2b0adbec3836842ba2&echostr=8648907200949385079&timestamp=1590113847&nonce=1122677967')
        data = response.get_data(as_text=True)
        self.assertNotEqual('', data)

    def test_text_post_handle(self):
        text_msg = '''
        <xml>
            <ToUserName><![CDATA[gh_5e0018d6e988]]></ToUserName>
            <FromUserName><![CDATA[opXMawEuGjdDDDBGZZhAsJBZmysE]]></FromUserName>
            <CreateTime>1590114356</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[测试文本消息]]></Content>
            <MsgId>22764966868465486</MsgId>
        </xml>
        '''
        url = '/wx?signature=f60f9796c2fb3303b54bcc85fc7c3d43decab712&timestamp=1590114356&nonce=1404715972&openid=opXMawEuGjdDDDBGZZhAsJBZmysE'
        response = self.client.post(url, data=text_msg)
        data = response.get_data(as_text=True)
        self.assertIn('测试文本消息', data)

    def test_image_post_handle(self):
        image_msg = '''
        <xml>
            <ToUserName><![CDATA[gh_5e0018d6e988]]></ToUserName>
            <FromUserName><![CDATA[opXMawEuGjdDDDBGZZhAsJBZmysE]]></FromUserName>
            <CreateTime>1590115005</CreateTime>
            <MsgType><![CDATA[image]]></MsgType>
            <PicUrl><![CDATA[http://mmbiz.qpic.cn/mmbiz_jpg/eznTX6UYyE0mnib3Gm1upkBBTplrgbzC7ya1tHhHrBR6CJ2zmuCFib16FqYDPbtP1ia8MRx97M7xN5l5dnFJhCd3w/0]]></PicUrl>
            <MsgId>22764973581403052</MsgId>
            <MediaId><![CDATA[YnA34-5GW508Bf55G8FC7GGByzhKg2e5ZyU8Av-zxuhaPwungC5aFG9xRXiEQZil]]></MediaId>
        </xml>
        '''
        url = '/wx?signature=a71b10186dabd9a0d9c850da92a5d95b17fdd171&timestamp=1590115006&nonce=1515151521&openid=opXMawEuGjdDDDBGZZhAsJBZmysE'
        response = self.client.post(url, data=image_msg)
        data = response.get_data(as_text=True)
        self.assertIn('YnA34-5GW508Bf55G8FC7GGByzhKg2e5ZyU8Av-zxuhaPwungC5aFG9xRXiEQZil', data)

    def test_location_post_handle(self):
        location_msg = '''
        <xml>
            <ToUserName><![CDATA[gh_5e0018d6e988]]></ToUserName>
            <FromUserName><![CDATA[opXMawEuGjdDDDBGZZhAsJBZmysE]]></FromUserName>
            <CreateTime>1590115829</CreateTime>
            <MsgType><![CDATA[location]]></MsgType>
            <Location_X>31.243330</Location_X>
            <Location_Y>121.519534</Location_Y>
            <Scale>15</Scale>
            <Label><![CDATA[测试location消息]]></Label>
            <MsgId>22764984982539304</MsgId>
        </xml>
        '''
        url = '/wx?signature=4a25f412913c87070004f207f794f5c55eee9103&timestamp=1590115829&nonce=1214904871&openid=opXMawEuGjdDDDBGZZhAsJBZmysE'
        response = self.client.post(url, data=location_msg)
        data = response.get_data(as_text=True)
        self.assertIn('opXMawEuGjdDDDBGZZhAsJBZmysE', data)

    def test_click_post_handle(self):
        click_msg = '''
            <xml>
                <ToUserName><![CDATA[gh_5e0018d6e988]]></ToUserName>
                <FromUserName><![CDATA[opXMawEuGjdDDDBGZZhAsJBZmysE]]></FromUserName>
                <CreateTime>1590117086</CreateTime>
                <MsgType><![CDATA[event]]></MsgType>
                <Event><![CDATA[CLICK]]></Event>
                <EventKey><![CDATA[mpGuide]]></EventKey>
            </xml>
        '''
        url = '/wx?signature=04c13a4a433dea70c610630e5964b0bb0291129f&timestamp=1590117086&nonce=1610840709&openid=opXMawEuGjdDDDBGZZhAsJBZmysE'
        response = self.client.post(url, data=click_msg)
        data = response.get_data(as_text=True)
        self.assertIn('mpGuide', data)

    def test_accesstoken(self):
        response = self.client.get('/wx/token')
        data = response.get_data(as_text=True)
        self.assertIsNotNone(data)



if __name__ == "__main__":
    unittest.main()