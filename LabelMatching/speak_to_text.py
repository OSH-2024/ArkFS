import speech_recognition as sr
#语音转文字


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
    except sr.RequestError as e:
        print("无法请求 Google Web Speech API; {0}".format(e))

    # 将文本转换为字符串
    text_str = str(text)

    # 检查是否包含“手动”
    if "手动" in text_str:
        text = input("请输入:")
    else:
        print(f"输入结果: {text_str}")

    return text
