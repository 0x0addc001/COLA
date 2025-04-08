import hmac
import time
import requests
from datetime import datetime
import hashlib
import uuid
import base64


class Text2img:
    def __init__(self, ak='2KzteqKTA2FnsLWREIsCNg', sk='uqaabYpXCh-uX6KiN_VRkjg30dlEN453', interval=5):
        """
        :param ak
        :param sk
        :param interval 轮询间隔
        """
        self.ak = ak
        self.sk = sk
        self.time_stamp = int(datetime.now().timestamp() * 1000)  # 毫秒级时间戳
        self.signature_nonce = uuid.uuid1()  # 随机字符串
        self.signature_img = self._hash_sk(self.sk, self.time_stamp, self.signature_nonce)
        self.signature_ultra_img = self._hash_ultra_sk(self.sk, self.time_stamp, self.signature_nonce)
        self.signature_status = self._hash_sk_status(self.sk, self.time_stamp, self.signature_nonce)
        self.interval = interval
        self.headers = {'Content-Type': 'application/json'}
        self.text2img_url = self.get_image_url(self.ak, self.signature_img, self.time_stamp,
                                               self.signature_nonce)
        self.text2img_ultra_url = self.get_ultra_image_url(self.ak, self.signature_ultra_img, self.time_stamp,
                                                           self.signature_nonce)
        self.generate_url = self.get_generate_url(self.ak, self.signature_status, self.time_stamp,
                                                  self.signature_nonce)

    def hmac_sha1(self, key, code):
        hmac_code = hmac.new(key.encode(), code.encode(), hashlib.sha1)
        return hmac_code.digest()

    def _hash_sk(self, key, s_time, ro):
        """加密sk"""
        data = "/api/generate/webui/text2img" + "&" + str(s_time) + "&" + str(ro)
        s = base64.urlsafe_b64encode(self.hmac_sha1(key, data)).rstrip(b'=').decode()
        return s

    def _hash_ultra_sk(self, key, s_time, ro):
        """加密sk"""
        data = "/api/generate/webui/text2img/ultra" + "&" + str(s_time) + "&" + str(ro)
        s = base64.urlsafe_b64encode(self.hmac_sha1(key, data)).rstrip(b'=').decode()
        return s

    def _hash_sk_status(self, key, s_time, ro):
        """加密sk"""
        data = "/api/generate/webui/status" + "&" + str(s_time) + "&" + str(ro)
        s = base64.urlsafe_b64encode(self.hmac_sha1(key, data)).rstrip(b'=').decode()
        return s

    def get_image_url(self, ak, signature, time_stamp, signature_nonce):

        url = f"https://openapi.liblibai.cloud/api/generate/webui/text2img?AccessKey={ak}&Signature={signature}&Timestamp={time_stamp}&SignatureNonce={signature_nonce}"
        return url

    def get_ultra_image_url(self, ak, signature, time_stamp, signature_nonce):

        url = f"https://openapi.liblibai.cloud/api/generate/webui/text2img/ultra?AccessKey={ak}&Signature={signature}&Timestamp={time_stamp}&SignatureNonce={signature_nonce}"
        return url

    def get_generate_url(self, ak, signature, time_stamp, signature_nonce):

        url = f"https://openapi.liblibai.cloud/api/generate/webui/status?AccessKey={ak}&Signature={signature}&Timestamp={time_stamp}&SignatureNonce={signature_nonce}"
        return url

    def ultra_text2img(self):
        """
        ultra json
        """
        base_json = {
            "templateUuid": "5d7e67009b344550bc1aa6ccbfa1d7f4",
            "generateParams": {
                "prompt": "Serendipity, Dream Tarot, very detailed, ultra high resolution, 32K UHD, best quality, masterpiece,",
                "aspectRatio": "portrait",
                "imgCount": 1,
            }
        }
        self.run(base_json, self.text2img_ultra_url)

    def text2img(self, prompt):
        """
        文生图全示例 json
        """
        base_json = {
            "templateUuid": "6f7c4652458d4802969f8d089cf5b91f",
            "generateParams": {
                "prompt": prompt,
                "negativePrompt": "ng_deepnegative_v1_75t,(badhandv4:1.2),EasyNegative,(worst quality:2),",
                "steps": 30,
                "width": 1024,
                "height": 1024,
                "imgCount": 1,
                "cfgScale": 3.5,
                "randnSource": 0,
                "seed": -1,
                "restoreFaces": 0,
                "additionalNetwork": [
                    {
                        "modelId": "558ceb5f26024dec9e5279999a225d9a",
                        "weight": 0.8
                    }
                ],
            }
        }
        self.run(base_json, self.text2img_url)

    def run(self, data, url, timeout=600):
        """
        发送任务到生图接口，直到返回image为止，失败抛出异常信息
        """
        start_time = time.time()  # 记录开始时间
        # 这里提交任务，校验是否提交成功，并且获取任务ID
        print(url)
        response = requests.post(url=url, headers=self.headers, json=data)
        response.raise_for_status()
        progress = response.json()
        if progress['code'] == 0:
            # 如果获取到任务ID，执行等待生图
            while True:
                current_time = time.time()
                if (current_time - start_time) > timeout:
                    print(f"{timeout}s任务超时，已退出轮询。")
                    return None

                generate_uuid = progress["data"]['generateUuid']
                data = {"generateUuid": generate_uuid}
                response = requests.post(url=self.generate_url, headers=self.headers, json=data)
                response.raise_for_status()
                progress = response.json()
                print(progress)

                if progress['data'].get('images') and any(
                        image for image in progress['data']['images'] if image is not None):
                    print("任务完成，获取到图像数据。")

                    # 提取 imageUrl
                    image_url = progress['data']['images'][0]['imageUrl']
                    print("Image URL:", image_url)

                    return progress

                print(f"任务尚未完成，等待 {self.interval} 秒...")
                time.sleep(self.interval)
        else:
            return f'任务失败,原因：code {progress["msg"]}'


def main():
    prompt = "Modern naturalistic public space landscape design, aerial view, golden hour lighting, featuring:\n"+ \
    "1. **Ecological Corridor**: Winding permeable concrete path with 'plant curtain' layers - Wisteria/Campsis vines above, Hibiscus/Hydrangea mid-layer, Carex groundcover. Preserved railway art installations referencing High Line Park's 'planted architecture' aesthetic.\n"+ \
    "2. **Central Lawn**: Mixed turfgrass (Poa pratensis + Lolium perenne) with seasonal ribbon planting: Crocus→Lythrum→Chrysanthemum→Camellia. Mobile seating with recycled concrete bases and FSC teak tops.\n"+ \
    "3. **Water Feature**: Tiered ecological water system - stainless steel fountain transitioning to rain garden with Phragmites/Iris/Nymphaea gradient. Anti-slip glass grating walkway revealing water purification process below.\n"+ \
    "4. **Cultural Pavilion**: Parametric steel canopy mimicking leaf venation, embedded with local ceramic motifs. Solar-powered interactive light wall casting dappled shadows.\n"+ \
    "5. **Border Treatment**: Three-layer noise-reduction planting (Podocarpus/Viburnum/Lagerstroemia) with translucent concrete walls featuring framed viewports.\n"+ \
    "**Details**:\n"+ \
    "- Seasonal plant transitions: Magnolia stellata→Viburnum macrocephalum→Cotinus coggygria→Chimonanthus praecox\n"+ \
    "- Sustainable materials: 30% recycled aggregate concrete + 70% local sandstone paving\n"+ \
    "- Photovoltaic glass pavilion roof with kinetic paving lighting\n"+ \
    "- Piet Oudolf-inspired naturalistic planting with structural trees (Celtis/Sapium), 'Limelight' hydrangeas, and Lysimachia nummularia groundcover\n"+ \
    "**Rendering Style**: Hyper-realistic daylight visualization with subtle lens flare, depth of field focusing on the water feature, 8K resolution showing texture details in materials and foliage. Include people casually enjoying spaces for scale."
    print(prompt)
    test = Text2img()
    test.text2img(prompt)


if __name__ == '__main__':
    main()


    # response = {
    #     'code': 0,
    #     'data': {
    #         'generateUuid': '0d91361c7eb94c868f84d5e6fd039c60',
    #         'generateStatus': 5,
    #         'percentCompleted': 1.0,
    #         'generateMsg': None,
    #         'pointsCost': 10,
    #         'accountBalance': 990,
    #         'images': [{
    #             'imageUrl': 'https://liblibai-tmp-image.liblib.cloud/img/0b0bae3956a14eab87ed6400a64b1ea7/96999f958ab0255fdaa026e99c6b0e26deec1f962ce3ef61957161292509ee8c.png',
    #             'seed': 3161442867,
    #             'auditStatus': 3
    #         }]
    #     },
    #     'msg': ''
    # }
    # # 提取 imageUrl
    # image_url = response['data']['images'][0]['imageUrl']
    # print("Image URL:", image_url)