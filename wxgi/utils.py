import hashlib


def check_wechat_signature(token, timestamp, nonce, signature):
    sorted_list = sorted((token, timestamp, nonce))
    sorted_str = ''.join(sorted_list)

    sha1 = hashlib.sha1(sorted_str.encode('utf-8'))
    
    return sha1.hexdigest() == signature

