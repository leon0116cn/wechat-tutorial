import hashlib
import requests
import redis
from wxgi import settings


def check_signature(token, timestamp, nonce, signature):
    sorted_list = sorted((token, timestamp, nonce))
    sorted_str = ''.join(sorted_list)

    sha1 = hashlib.sha1(sorted_str.encode('utf-8'))
    hashcode = sha1.hexdigest()

    print('handle/GET fun: hashcode, signature: ', hashcode, signature)
    
    return hashcode == signature


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