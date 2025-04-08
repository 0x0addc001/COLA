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

    def text2img(self):
        """
        文生图全示例 json
        """
        base_json = {
            "templateUuid": "e10adc3949ba59abbe56e057f20f883e",
            "generateParams": {
                "checkPointId": "0ea388c7eb854be3ba3c6f65aac6bfd3",
                "vaeId": "",
                "prompt": "Asian portrait,A young woman wearing a green baseball cap,covering one eye with her hand",
                "negativePrompt": "bad-artist, bad-artist-anime, bad-hands-5, bad-image-v2-39000, bad-picture-chill-75v, bad_prompt, bad_prompt_version2, badhandv4, NG_DeepNegative_V1_75T, EasyNegative,2girls, 3girls,,bad quality, poor quality, doll, disfigured, jpg, toy, bad anatomy, missing limbs, missing fingers, 3d, cgi",
                "width": 768,
                "height": 1024,
                "imgCount": 1,
                "cfgScale": 7,
                "randnSource": 0,
                "seed": -1,
                "clipSkip": 2,
                "sampler": 15,
                "steps": 20,
                "restoreFaces": 0,
                "additionalNetwork": [
                    {
                        "modelId": "3dc63c4fe3df4147ac8a875db3621e9f",
                        "weight": 0.6
                    }
                ],
                "hiResFixInfo": {
                    "hiresDenoisingStrength": 0.75,
                    "hiresSteps": 20,
                    "resizedHeight": 1536,
                    "resizedWidth": 1024,
                    "upscaler": 10
                },
                "controlNet": [
                    {
                        "unitOrder": 0,
                        "sourceImage": "https://liblibai-online.liblib.cloud/img/081e9f07d9bd4c2ba090efde163518f9/7c1cc38e-522c-43fe-aca9-07d5420d743e.png",
                        "width": 1024,
                        "height": 1536,
                        "preprocessor": 3,
                        "annotationParameters": {
                            "depthLeres": {
                                "preprocessorResolution": 1024,
                                "removeNear": 0,
                                "removeBackground": 0
                            }
                        },
                        "model": "6349e9dae8814084bd9c1585d335c24c",
                        "controlWeight": 1,
                        "startingControlStep": 0,
                        "endingControlStep": 1,
                        "pixelPerfect": 1,
                        "controlMode": 0,
                        "resizeMode": 1,
                        "maskImage": ""
                    }
                ]
            }
        }
        self.run(base_json, self.text2img_url)

    def run(self, data, url, timeout=120):
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
                    return progress

                print(f"任务尚未完成，等待 {self.interval} 秒...")
                time.sleep(self.interval)
        else:
            return f'任务失败,原因：code {progress["msg"]}'


def main():
    test = Text2img()
    # 简易模式：旗舰版任务，如果不需要请注释
    test.ultra_text2img()
    # 进阶模式：最全版本文生图，如果不需要请注释（API标准计划可用）
    test.text2img()


if __name__ == '__main__':
    main()