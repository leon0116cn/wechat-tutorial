import requests
import redis
from wxgi import settings


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
        except ValueError as e:
            print('No json object return!')

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
