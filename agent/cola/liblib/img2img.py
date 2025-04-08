import hmac
import time
import requests
from datetime import datetime
import hashlib
import uuid
import base64


class Img2img:
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
        self.img2img_url = self.get_image_url(self.ak, self.signature_img, self.time_stamp,
                                              self.signature_nonce)
        self.img2img_ultra_url = self.get_ultra_image_url(self.ak, self.signature_ultra_img, self.time_stamp,
                                                          self.signature_nonce)
        self.generate_url = self.get_generate_url(self.ak, self.signature_status, self.time_stamp,
                                                  self.signature_nonce)

    def hmac_sha1(self, key, code):
        hmac_code = hmac.new(key.encode(), code.encode(), hashlib.sha1)
        return hmac_code.digest()

    def _hash_sk(self, key, s_time, ro):
        """加密sk"""
        data = "/api/generate/webui/img2img" + "&" + str(s_time) + "&" + str(ro)
        s = base64.urlsafe_b64encode(self.hmac_sha1(key, data)).rstrip(b'=').decode()
        return s

    def _hash_ultra_sk(self, key, s_time, ro):
        """加密sk"""
        data = "/api/generate/webui/img2img/ultra" + "&" + str(s_time) + "&" + str(ro)
        s = base64.urlsafe_b64encode(self.hmac_sha1(key, data)).rstrip(b'=').decode()
        return s

    def _hash_sk_status(self, key, s_time, ro):
        """加密sk"""
        data = "/api/generate/webui/status" + "&" + str(s_time) + "&" + str(ro)
        s = base64.urlsafe_b64encode(self.hmac_sha1(key, data)).rstrip(b'=').decode()
        return s

    def get_image_url(self, ak, signature, time_stamp, signature_nonce):

        url = f"https://openapi.liblibai.cloud/api/generate/webui/img2img?AccessKey={ak}&Signature={signature}&Timestamp={time_stamp}&SignatureNonce={signature_nonce}"
        return url

    def get_ultra_image_url(self, ak, signature, time_stamp, signature_nonce):

        url = f"https://openapi.liblibai.cloud/api/generate/webui/img2img/ultra?AccessKey={ak}&Signature={signature}&Timestamp={time_stamp}&SignatureNonce={signature_nonce}"
        return url

    def get_generate_url(self, ak, signature, time_stamp, signature_nonce):

        url = f"https://openapi.liblibai.cloud/api/generate/webui/status?AccessKey={ak}&Signature={signature}&Timestamp={time_stamp}&SignatureNonce={signature_nonce}"
        return url

    def ultra_img2img(self):
        """
        ultra json
        """
        base_json = {
            "templateUuid": "07e00af4fc464c7ab55ff906f8acf1b7",
            "generateParams": {
                "prompt": "filmfotos, 1 asian girl with beautiful face,lotus leaf,masterpiece,best quality,finely detail,highres,8k,beautiful and aesthetic,no watermark,",
                "imgCount": 1,
                "sourceImage": "https://liblibai-online.liblib.cloud/img/081e9f07d9bd4c2ba090efde163518f9/7c1cc38e-522c-43fe-aca9-07d5420d743e.png",
            }
        }
        self.run(base_json, self.img2img_ultra_url)

    def img2img(self):
        """
        图生图全示例 json
        """
        base_json = {
            "templateUuid": "9c7d531dc75f476aa833b3d452b8f7ad",
            "generateParams": {
                "checkPointId": "0ea388c7eb854be3ba3c6f65aac6bfd3",
                "prompt": "彩虹，",
                "negativePrompt": "下雨,easynegative,badhandv4",
                "imgCount": 1,
                "cfgScale": 15,
                "randnSource": 0,
                "seed": -1,
                "clipSkip": 1,
                "sampler": 1,
                "steps": 10,
                "restoreFaces": 1,
                "resizeMode": 1,
                "resizedWidth": 512,
                "resizedHeight": 768,
                "mode": 0,
                "denoisingStrength": 1,
                "sourceImage": "https://liblibai-models.oss-cn-beijing.aliyuncs.com/img/9f9178b9593b4ba7b42739c77b1b4958/459c890fe76a4426e060f208392b27df70685f99465d596731bcd37c8d91c06b.jpg",
                "additionalNetwork": [
                    {
                        "modelId": "1fe2174f51d04fedb724b28f48d55b7a",
                        "weight": 0.6
                    }
                ],
                "controlNet": [
                    {
                        "unitOrder": 0,
                        "controlWeight": 1,
                        "startingControlStep": 0,
                        "endingControlStep": 1,
                        "pixelPerfect": 1,
                        "controlMode": 0,
                        "resizeMode": 1,
                        "preprocessor": 3,
                        "annotationParameters": {
                            "depthLeres": {
                                "preprocessorResolution": 1024,
                                "removeNear": 0,
                                "removeBackground": 0
                            }
                        },
                        "model": "dccde738064e9748f93b48ec5868968e",
                        "width": 512,
                        "height": 1536,
                        "sourceImage": "https://liblibai-models.oss-cn-beijing.aliyuncs.com/img/9f9178b9593b4ba7b42739c77b1b4958/459c890fe76a4426e060f208392b27df70685f99465d596731bcd37c8d91c06b.jpg",
                        "maskImage": "https://liblibai-gen-images.oss-cn-beijing.aliyuncs.com/img/9f9178b9593b4ba7b42739c77b1b4958/17974823534284a61d0c95898e6df05a71c6eb2727a374d06c894b58929f8c08.jpg"
                    }
                ]
            }
        }
        self.run(base_json, self.img2img_url)

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
                    return progress

                print(f"任务尚未完成，等待 {self.interval} 秒...")
                time.sleep(self.interval)
        else:
            return f'任务失败,原因：code {progress["msg"]}'


def main():
    test = Img2img()
    # 简易模式：旗舰版任务，如果不需要请注释
    test.ultra_img2img()
    # 进阶模式：最全版本图生图，如果不需要请注释（API标准计划可用）
    test.img2img()


if __name__ == '__main__':
    main()

