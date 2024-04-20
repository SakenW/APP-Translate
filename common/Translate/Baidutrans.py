import http.client
import hashlib
import urllib
import random
import json

class BaiduFieldTranslate:
    def __init__(self, appid, secret_key):
        """
        初始化百度翻译 API 客户端。

        参数:
        - appid: 百度翻译 API 的 APP ID。
        - secret_key: 百度翻译 API 的密钥。
        """
        self.appid = appid
        self.secret_key = secret_key

    def translate(self, text, dest_language, domain):
        """
        使用百度领域翻译 API 翻译文本。

        参数:
        - text (str): 待翻译的文本。
        - dest_language (str): 目标语言的 ISO 639-1 语言代码。
        - domain (str): 翻译领域，用于改善翻译准确性。

        返回:
        - str: 翻译后的文本。
        """
        salt = random.randint(32768, 65536)
        sign = self.appid + text + str(salt) + domain + self.secret_key
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = f'/api/trans/vip/fieldtranslate?appid={self.appid}&q={urllib.parse.quote(text)}&from=auto&to={dest_language}&salt={salt}&domain={domain}&sign={sign}'

        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)

            # 获取HTTPResponse对象
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)

            if "trans_result" in result:
                return result["trans_result"][0]["dst"]
            else:
                print("翻译错误：", result.get("error_msg", "未知错误"))
                return None
        except Exception as e:
            print(f"翻译时出现错误：{e}")
            return None
        finally:
            if httpClient:
                httpClient.close()

# 示例调用
if __name__ == "__main__":
    # 创建翻译器实例，这里的 appid 和 secretKey 需要替换为你的
    translator = BaiduFieldTranslate('20231113001878182', 'kS42zVyhZfcXW67hX9_Y')
    
    # 待翻译的文本
    text_to_translate = "crop"
    
    # 目标语言
    target_language = "zh"
    
    # 领域
    domain = "it"
    
    # 执行翻译
    translated_text = translator.translate(text_to_translate, target_language, domain)
    
    # 打印翻译结果
    print(f"翻译结果：{translated_text}")
