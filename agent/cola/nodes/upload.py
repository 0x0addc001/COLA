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

