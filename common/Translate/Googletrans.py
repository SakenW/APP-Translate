# 文件路径: common/Translate/Googletrans.py

from googletrans import Translator, LANGCODES

class GoogleTranslate:
    def __init__(self):
        self.translator = Translator()

    def translate(self, text, dest_language, software_name, context="Content in the software"):
        """
        翻译文本到指定语言，可选加上上下文以提升翻译准确性。
        
        参数:
            text (str): 待翻译的文本。
            dest_language (str): 目标语言的ISO 639-1语言代码。
            context (str, optional): 翻译上下文，用于提升翻译准确性。

        返回:
            str: 翻译后的文本，不包含上下文信息。
        """
        start_marker = "[<+]"
        end_marker = "[+>]"
        full_text = f"{start_marker}{context}:{end_marker}{text}" if context else text
        dest_language = dest_language.replace('_', '-').lower()

        if dest_language not in LANGCODES.values():
            raise ValueError(f"不支持的语言代码：{dest_language}")

        try:
            result = self.translator.translate(full_text, dest=dest_language)
            # 移除标记及其之前的所有内容和之后的所有内容
            translated_text = result.text.split(end_marker)[-1] if end_marker in result.text else result.text
            return translated_text.strip()
        except Exception as e:
            print(f"翻译时出现错误：{e}")
            return None


# 示例调用
if __name__ == "__main__":
    # 创建翻译器实例
    translator = GoogleTranslate()
    
    # 待翻译的文本
    text_to_translate = "crop"
    
    # 目标语言
    target_language = "zh_CN"  # 中文简体
    
    # 软件名称
    software_name = "DEVONthink"
    
    # 执行翻译
    translated_text = translator.translate(text_to_translate, target_language, software_name)
    
    # 打印翻译结果
    print(f"原文：{text_to_translate}\n翻译：{translated_text}")

