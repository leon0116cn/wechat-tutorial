import requests
from wxgi import settings
from wxgi.basic import WechatAccessToken


class WechatMenu:
    def create(self, post_data, access_token):
        try:
            r = requests.post(
                settings.WECHAT_CREATE_MENU_URL,
                params={'access_token': access_token},
                json=post_data,
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

        if resp_data.get('errcode') != 0:
            print(resp_data.get('errcode'))
            print(resp_data.get('errmsg'))
            return False

        return True

    def get_current_menu(self, access_token):
        try:
            r = requests.get(
                settings.WECHAT_CURRENT_MENU_URL, 
                params={'access_token': access_token}, 
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

        return resp_data

    def delete(self, access_token):
        try:
            r = requests.get(
                settings.WECHAT_DELETE_MENU_URL, 
                params={'access_token': access_token}, 
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
        
        if resp_data.get('errcode') != 0:
            print(resp_data.get('errcode'))
            print(resp_data.get('errmsg'))
            return False

        return True
