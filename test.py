import xml.etree.ElementTree as ET


if __name__ == "__main__":
    xml_doc = '''
    <xml>
        <ToUserName><![CDATA[gh_5e0018d6e988]]></ToUserName>
        <FromUserName><![CDATA[opXMawEuGjdDDDBGZZhAsJBZmysE]]></FromUserName>
        <CreateTime>1590044727</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[location_select]]></Event>
        <EventKey><![CDATA[myLocation]]></EventKey>
        <SendLocationInfo>
            <Location_X><![CDATA[31.243673324584961]]></Location_X>
            <Location_Y><![CDATA[121.51815795898438]]></Location_Y>
            <Scale><![CDATA[15]]></Scale>
            <Label><![CDATA[label]]></Label>
            <Poiname><![CDATA[poiname]]></Poiname>
        </SendLocationInfo>
    </xml>
    '''
    data = ET.fromstring(xml_doc)
    text = data.find('Location_X').text
    print(text)