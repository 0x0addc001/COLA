import hmac
from hashlib import sha1
import base64
import time
import uuid


def make_sign():
    """
    生成签名
    """

    # API密钥的ID
    access_key = '2KzteqKTA2FnsLWREIsCNg' # 这里是示例，实际使用的时候需要替换成实际的access_key

    # API访问密钥
    secret_key = 'uqaabYpXCh-uX6KiN_VRkjg30dlEN453' # 这里是示例，实际使用的时候需要替换成实际的secret_key

    # 请求API接口的uri地址
    uri = "/api/model/version/get" # 这里是示例，实际使用的时候需要替换成实际的uri地址
    # 当前毫秒时间戳
    timestamp = str(int(time.time() * 1000))
    print("timestamp:", timestamp)
    # 随机字符串
    signature_nonce = str(uuid.uuid4())
    print("signature_nonce:", signature_nonce)
    # 拼接请求数据
    content = '&'.join((uri, timestamp, signature_nonce))
    # 生成签名
    digest = hmac.new(secret_key.encode(), content.encode(), sha1).digest()
    # 移除为了补全base64位数而填充的尾部等号
    sign = base64.urlsafe_b64encode(digest).rstrip(b'=').decode()
    print("sign:", sign)
    return sign

if __name__ == '__main__':
    make_sign()