import hashlib
import json
import requests
from wxgi import settings


def check_signature(token, timestamp, nonce, signature):
    sorted_list = sorted((token, timestamp, nonce))
    sorted_str = ''.join(sorted_list)

    sha1 = hashlib.sha1(sorted_str.encode('utf-8'))
    
    return sha1.hexdigest() == signature


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
    except ValueError as e:
        print('No json object return!')
    
    if 'errcode' in resp_data:
        print('Wechat return error!')
        print(access_token.get('errcode'), access_token.get('errmsg'))
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
    except ValueError as e:
        print('No json object return!')
    
    if 'errcode' in resp_data:
        print('Wechat return error!')
        print(access_token.get('errcode'), access_token.get('errmsg'))
        return None

    return resp_data.get('ip_list')


def create_menu(token, path):
    with open(path, 'r', encoding='utf-8') as f:
        menu = json.load(f)

    try:
        r = requests.post(
            settings.WECHAT_CREATE_MENU_URL,
            params={'access_token': token},
            json=menu,
            timeout=10
        )
        r.raise_for_status()
        resp_data = r.json()
    except requests.HTTPError as e:
        print('Wechat connection error!')
    except ValueError as e:
        print('No json object return!')

    
    if resp_data.get('errcode') != 0:
        print(resp_data.get('errcode'))
        print(resp_data.get('errmsg'))
        return False

    return True


def delete_menu(token):
    try:
        r = requests.get(
            settings.WECHAT_DELETE_MENU_URL, 
            params={'access_token': token}, 
            timeout=10
            )
        r.raise_for_status()
        resp_data = r.json()
    except requests.HTTPError as e:
        print('Wechat connection error!')
    except ValueError as e:
        print('No json object return!')
    
    if resp_data.get('errcode') != 0:
        print(resp_data.get('errcode'))
        print(resp_data.get('errmsg'))
        return False

    return True


def current_menu(token):
    try:
        r = requests.get(
            settings.WECHAT_CURRENT_MENU_URL, 
            params={'access_token': token}, 
            timeout=10
            )
        r.raise_for_status()
        resp_data = r.json()
    except requests.HTTPError as e:
        print('Wechat connection error!')
    except ValueError as e:
        print('No json object return!')

    return resp_data

