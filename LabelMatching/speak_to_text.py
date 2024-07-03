import speech_recognition as sr
#语音转文字
from datetime import datetime, timedelta

def recognize_speech_from_mic():
    # 获取默认的麦克风
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # 从麦克风录音
    with microphone as source:
        print("请说话...(“手动输入”则切换为手动输入)")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # 使用 Google Web Speech API 将音频转换为文本
    try:
        print("识别中...")
        text = recognizer.recognize_google(audio, language='zh-CN')
    except sr.UnknownValueError:
        print("Speech无法理解音频")
        print("手动输入")
        text = input("请输入:")
    except sr.RequestError as e:
        print("无法请求 Google Web Speech API; {0}".format(e))
        

    # 将文本转换为字符串
    text_str = str(text)

#    # 检查是否包含“手动”
#    if "手动" in text_str:
#        text = input("请输入:")
#    else:
#        print(f"输入结果: {text_str}")
#
    print(f"输入结果: {text_str}")
    
    return text


def map_relative_time_to_iso(time_str):
    """
    Map relative time descriptors to ISO 8601 format.

    Parameters:
        time_str (str): Relative time descriptor (e.g., '昨天', '前天', '大前天').

    Returns:
        str: ISO 8601 formatted date string.
    """
    now = datetime.now()
    
    if time_str == "昨天":
        start_time = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = now
    elif time_str == "前天":
        start_time = (now - timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_str == "大前天":
        start_time = (now - timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = (now - timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_str == "今天":
        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = now
    elif time_str=="一周内":
        start_time = (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = now
    elif time_str=="一个月内":
        start_time = (now - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = now
    elif time_str=="一年内":
        start_time = (now - timedelta(days=365)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = now
    elif time_str=="一小时内":
        start_time = (now - timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        end_time = now
    elif time_str=="两小时内":
        start_time = (now - timedelta(hours=2)).replace(minute=0, second=0, microsecond=0)
        end_time = now
    elif time_str=="三小时内":
        start_time = (now - timedelta(hours=3)).replace(minute=0, second=0, microsecond=0)
        end_time = now
    else:
        return "NULL", "NULL"
    
    return [start_time.isoformat(), end_time.isoformat()]