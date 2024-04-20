import requests
import json
from time import sleep
from requests.exceptions import RequestException

class OpenAITranslate:
    def __init__(self, api_key):
        # 初始化，设置 API 密钥和请求头部
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        self.url = "https://api.openai-hk.com/v1/chat/completions"

    def translate(self, text, dest_language, software_name, retries=3, timeout=10):
        # 构造翻译请求的提示文本
        prompt = f"For software localization to {dest_language}, translate and return only:/n/n{text}"
        # 准备请求的数据
        data = {
            "model": "gpt-3.5-turbo-1106",  # 根据实际情况调整模型
            "temperature": 0.8,
            "max_tokens": 120,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个由OpenAI训练的翻译模型。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        for attempt in range(retries):
            try:
                # 发起POST请求
                response = requests.post(self.url, headers=self.headers, data=json.dumps(data).encode('utf-8'), timeout=timeout)
                response.raise_for_status()  # 如果响应状态码不是200系列，则抛出异常
                result = response.json()
                messages = result.get('choices', [])[0].get('message', {}).get('content', '')
                return messages
            except RequestException as e:
                # 处理请求异常，例如：网络问题或服务端问题
                print(f"尝试{attempt + 1}失败: {e}")
                if attempt < retries - 1:
                    # 实施指数退避策略，延迟重试
                    sleep_time = 2 ** attempt
                    print(f"{sleep_time}秒后重试...")
                    sleep(sleep_time)
                else:
                    print("达到最大重试次数，放弃重试。")
            except Exception as e:
                # 处理其他可能的异常
                print(f"发生错误: {e}")
                return None

# 示例使用
if __name__ == "__main__":
    api_key = ""
    translator = OpenAITranslate(api_key)
    text_to_translate = "Crop"
    target_language = "zh-CN"  # 假设服务需要目标语言的全名或其他标识符
    software_name = "DEVONthink"
    translated_text = translator.translate(text_to_translate, target_language, software_name)
    print(f"原文: {text_to_translate}\n翻译: {translated_text}")
