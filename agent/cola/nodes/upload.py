"""
import requests

# 注册账号：https://imgur.com/
# 申请 API Client ID：https://api.imgur.com/oauth2/addclient
# 使用 POST 请求上传图像，获取返回的图像公网链接。

client_id = '8332780eb92896b'
client_secret = '7c4778e526c25a60576cb57981d77e9450fe3564'
headers = {'Authorization': f'Client-ID {client_id}'}

# image_path = 'test.jpg'  # 本地图像路径
async def upload_image(image_path):
    with open(image_path, 'rb') as img:
        response = requests.post(
            url="https://api.imgur.com/3/image",
            headers=headers,
            files={'image': img}
        )
    data = response.json()
    if data['success']:
        print('公网链接:', data['data']['link'])
        return data['data']['link']
    else:
        print('上传失败:', data)
        return None
"""


# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import os
import logging

# 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 1. 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在 CosConfig 中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
# secret_id = os.environ['COS_SECRET_ID']     # 用户的 SecretId，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
# # secret_key = os.environ['COS_SECRET_KEY']   # 用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
secret_id = 'AKIDkMpongR0NbcdaMwJTggVUKzSjonZ7SaU'
secret_key = 'lIckflfOxJSffR1NYYM3c8tdEdpsnW5l'


region = 'ap-beijing'  # 替换为用户的 region，已创建桶归属的 region 可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
                           # COS 支持的所有 region 列表参见 https://cloud.tencent.com/document/product/436/6224
token = None               # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
scheme = 'https'           # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)

# #### 文件流简单上传（不支持超过5G的文件，推荐使用下方高级上传接口）
# # 强烈建议您以二进制模式(binary mode)打开文件,否则可能会导致错误
# with open('picture.jpg', 'rb') as fp:
#     response = client.put_object(
#         Bucket='examplebucket-1250000000',
#         Body=fp,
#         Key='picture.jpg',
#         StorageClass='STANDARD',
#         EnableMD5=False
#     )
# print(response['ETag'])
#
# #### 字节流简单上传
# response = client.put_object(
#     Bucket='examplebucket-1250000000',
#     Body=b'bytes',
#     Key='picture.jpg',
#     EnableMD5=False
# )
# print(response['ETag'])
#
#
# #### chunk 简单上传
# import requests
# stream = requests.get('https://cloud.tencent.com/document/product/436/7778')
#
# # 网络流将以 Transfer-Encoding:chunked 的方式传输到 COS
# response = client.put_object(
#     Bucket='examplebucket-1250000000',
#     Body=stream,
#     Key='picture.jpg'
# )
# print(response['ETag'])
#
# #### 高级上传接口（推荐）
# # 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
# response = client.upload_file(
#     Bucket='test-1313295794',
#     LocalFilePath=r'D:\ThesisProjects\COLA\test\test-1.png',
#     Key='test-1.png',
#     PartSize=1,
#     MAXThread=10,
#     EnableMD5=False
# )
# print(response['ETag'])
# INFO:qcloud_cos.cos_client:generate built-in connection pool success. maxsize=10,10
# INFO:qcloud_cos.cos_client:bound built-in connection pool when new client. maxsize=10,10
# INFO:qcloud_cos.cos_client:put object, url=:https://test-1313295794.cos.ap-beijing.myqcloud.com/test-1.png ,headers=:{}
# "1737819eb812952405d1d23a2e46e9a9"

image_path = 'test-1.png'

# # -*- coding=utf-8
# from qcloud_cos import CosConfig
# from qcloud_cos import CosS3Client
# import sys
# import os
# import logging
import requests

# # 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
# logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#
# # 1. 设置用户属性, 包括 secret_id, secret_key, region 等。Appid 已在 CosConfig 中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
# secret_id = os.environ['COS_SECRET_ID']     # 用户的 SecretId，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
# secret_key = os.environ['COS_SECRET_KEY']   # 用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
# region = 'ap-beijing'      # 替换为用户的 region，已创建桶归属的 region 可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
#                            # COS 支持的所有 region 列表参见 https://cloud.tencent.com/document/product/436/6224
# token = None               # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
# scheme = 'https'           # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
#
# config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# client = CosS3Client(config)
#
# # 生成URL
# url = client.get_object_url(
#     Bucket='test-1313295794',
#     Key='test-1.png'
# )
# print(url)
#
# # 使用URL
# response = requests.get(url)
# print(response)


import random
import string

def generate_random_string(length):
    letters = string.ascii_letters + string.digits  # 可以根据需要添加其他字符集合，如 string.punctuation
    return ''.join(random.choice(letters) for _ in range(length))

# # 示例 生成长度为 10 的随机字符串
# random_string = generate_random_string(10)
# print(random_string)

import os

def get_file_extension(filename):
    """
    获取文件的后缀名（不包括点号），若无后缀则返回空字符串。
    """
    return os.path.splitext(filename)[1][1:]

# 示例
# print(get_file_extension("example.txt"))      # 输出: txt
# print(get_file_extension("archive.tar.gz"))   # 输出: gz
# print(get_file_extension("README"))           # 输出: （空字符串）


async def upload_image(image_path):
    #### 高级上传接口（推荐）
    # 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。

    random_string = generate_random_string(10)
    generated_key=random_string+"."+get_file_extension(image_path)
    print(generated_key)

    response = client.upload_file(
        Bucket='test-1313295794',
        LocalFilePath=image_path,
        Key=generated_key,
        PartSize=1,
        MAXThread=10,
        EnableMD5=False
    )
    print(response['ETag'])
    # 生成URL
    url = client.get_object_url(
        Bucket='test-1313295794',
        Key=generated_key
    )
    return url
