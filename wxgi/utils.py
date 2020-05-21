import hashlib
import json
import xml.etree.ElementTree as ET
import requests
from wxgi import settings
from wxgi import models


def check_signature(token, timestamp, nonce, signature):
    sorted_list = sorted((token, timestamp, nonce))
    sorted_str = ''.join(sorted_list)

    sha1 = hashlib.sha1(sorted_str.encode('utf-8'))
    hashcode = sha1.hexdigest()

    print('handle/GET fun: hashcode, signature: ', hashcode, signature)
    
    return hashcode == signature


def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    
    xml_data = ET.fromstring(web_data)
    msg_type = xml_data.find('MsgType').text

    if msg_type == 'text':
        return models.TextWechatMsg(xml_data)
    elif msg_type == 'image':
        return models.ImageWechatMsg(xml_data)


def callback_ip(token):
    try:
        r = requests.get(
            settings.WECHAT_CALLBACK_IP_URL, 
            params={'access_token': token}, 
            timeout=10
            )
        r.raise_for_status()
        resp_data = r.json()
    except requests.HTTPError as e:
        print('Wechat connection error!')
        print(e)
    except ValueError as e:
        print('No json object return!')
        print(e)
    
    if 'errcode' in resp_data:
        print('Wechat return error!')
        print(resp_data.get('errcode'), resp_data.get('errmsg'))
        return None

    return resp_data.get('ip_list')


def api_domain_ip(token):
    try:
        r = requests.get(
            settings.WECHAT_API_DOMAIN_IP_URL, 
            params={'access_token': token}, 
            timeout=10
            )
        r.raise_for_status()
        resp_data = r.json()
    except requests.HTTPError as e:
        print('Wechat connection error!')
        print(e)
    except ValueError as e:
        print('No json object return!')
        print(e)
    
    if 'errcode' in resp_data:
        print('Wechat return error!')
        print(resp_data.get('errcode'), resp_data.get('errmsg'))
        return None

    return resp_data.get('ip_list')
    