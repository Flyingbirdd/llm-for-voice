# Step 1: Import necessary libraries and modules
import warnings
import pyaudio  
import wave  
import whisper  
import openai  
import keyboard  
import os  
import pyttsx3  
import tkinter as tk  
from tkinter import simpledialog  

# Step 2: Initialize Text-to-Speech engine (Windows users only)
# 初始化 pyttsx3 引擎用于文本转语音
engine = pyttsx3.init()
# 设置语音为 Windows 系统中的 Hazel 女声
hazel_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0"
engine.setProperty('voice', hazel_voice_id)
# 使用文本转语音引擎播放一段欢迎语音
engine.say("Hello Videotronic Maker, How can I assist you today sir?")
engine.runAndWait()

# Step 3: Define ANSI escape sequences for text color
# 定义 ANSI 转义序列，用于在终端打印彩色文本
colors = {
    "blue": "\033[94m",  
    "bright_blue": "\033[96m",  
    "orange": "\033[93m",  
    "yellow": "\033[93m", 
    "white": "\033[97m",  
    "red": "\033[91m",  
    "magenta": "\033[35m",  
    "bright_magenta": "\033[95m",  
    "cyan": "\033[36m",  
    "bright_cyan": "\033[96m",  
    "green": "\033[32m",  
    "bright_green": "\033[92m",  
    "reset": "\033[0m"  # 重置颜色
}

# Step 4: Ignore FP16 warnings
# 忽略与 FP16（16 位浮点数）相关的警告信息
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

# Step 5: Point to LM Studio Local Inference Server
# 配置本地推理服务器地址，并不需要 API 密钥
openai.api_base = "http://localhost:1234/v1"
openai.api_key = "not-needed"

# Step 6: Load the Whisper model
# 加载 Whisper 语音识别模型（使用最小版本“tiny”）
whisper_model = whisper.load_model("tiny")  # orig=base

# Step 7: Define audio parameters
# 设置音频参数
FORMAT = pyaudio.paInt16  # 设置音频格式为 16 位整数
CHANNELS = 1  # 设置音频通道为单声道
RATE = 8000  # 设置采样率为 8000 Hz
CHUNK = 1024  # 设置每次读取的音频块大小为 1024
audio = pyaudio.PyAudio()  # 初始化 PyAudio

# Step 8: Define function to speak text
# 定义一个将文本转为语音的函数
def speak(text):
    engine.say(text)  # 让文本转为语音
    engine.runAndWait()  # 等待语音播放完成

# Step 9: Define function to record audio
# 定义一个录制音频的函数
def record_audio():
    # 打开音频流，设置格式、通道数、采样率和缓冲区大小
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print(f"{colors['green']}Start speaking... (Press 'N' to stop){colors['reset']}")  # 提示用户开始说话
    frames = []  # 用于存储录音数据

    # 持续录音，直到用户按下 'N' 键
    while True:
        data = stream.read(CHUNK)  # 读取音频数据
        frames.append(data)  # 将数据添加到 frames 列表
        if keyboard.is_pressed('n'):  # 按下 'N' 键停止录音
            print(f"{colors['red']}Stopping recording.{colors['reset']}")
            break

    stream.stop_stream()  # 停止音频流
    stream.close()  # 关闭音频流

    # 保存录音文件为 WAV 格式
    wf = wave.open("temp_audio.wav", 'wb')
    wf.setnchannels(CHANNELS)  # 设置通道数
    wf.setsampwidth(audio.get_sample_size(FORMAT))  # 设置音频采样宽度
    wf.setframerate(RATE)  # 设置采样率
    wf.writeframes(b''.join(frames))  # 将音频数据写入文件
    wf.close()

    return "temp_audio.wav"  # 返回音频文件名

# Step 10: Define function to get user input via GUI dialog
# 定义一个通过 GUI 弹出对话框获取用户输入的函数
def get_user_input():
    ROOT = tk.Tk()  # 创建一个 Tkinter 根窗口
    ROOT.withdraw()  # 隐藏根窗口
    # 弹出输入框获取用户输入
    user_input = simpledialog.askstring(title="Text Input", prompt="Type your input:")
    return user_input  # 返回用户输入的文本

# Step 11: Define function to process user input and generate response
# 定义一个处理用户输入并生成响应的函数
def process_input(input_text):
    # 定义对话内容，包括系统和用户的消息
    conversation = [
        {"role": "system", "content": "You are KITT, the assistant chatbot. My name is VideotronicMaker, the human and user. Your role is to assist the human, who is known as VideotronicMaker. Respond concisely and accurately, maintaining a friendly, respectful, and professional tone. Emphasize honesty, candor, and precision in your responses."},
        {"role": "user", "content": input_text}  # 用户的输入文本
    ]

    # 调用本地推理模型生成响应
    completion = openai.ChatCompletion.create(
        model="local-model",  # 使用本地模型
        messages=conversation,  # 传入对话内容
        temperature=0.7,  # 控制生成文本的随机性
        top_p=0.9,  # 控制生成文本的多样性
        top_k=40  # 限制生成时的候选词数量
    )

    # 获取生成的响应内容
    assistant_reply = completion.choices[0].message.content
    print(f"{colors['magenta']}KITT:{colors['reset']} {assistant_reply}")  # 打印助手的回答
    speak(assistant_reply)  # 将助手的回答转为语音并播放

# Step 12: Main loop to continuously monitor for user input
# 主循环，持续监控用户输入
print(f"{colors['yellow']}Ready to record. (Press 'B' to start, 'M' to type){colors['reset']}")
while True:
    try:
        if keyboard.is_pressed('b'): 
            audio_file = record_audio()  # 录制音频
            transcribe_result = whisper_model.transcribe(audio_file)  # 使用 Whisper 模型转录音频
            transcribed_text = transcribe_result["text"]  # 获取转录的文本
            print(f"{colors['blue']}VTM:{colors['reset']} {transcribed_text}")  # 打印转录文本
            process_input(transcribed_text)  # 处理转录的文本并生成响应
            os.remove(audio_file)  # 删除临时音频文件

        elif keyboard.is_pressed('m'):
            typed_input = get_user_input()  # 获取用户输入的文本
            if typed_input:  # 确保输入不为空
                print(f"{colors['blue']}VTM typed:{colors['reset']} {typed_input}")  # 打印输入的文本
                process_input(typed_input)  # 处理输入并生成响应

    except KeyboardInterrupt:  # 捕捉键盘中断（Ctrl+C）
        print("\nExiting...")
        break  # 正常退出循环

# Step 13: Cleanup audio resources
# 清理和释放音频资源
audio.terminate()
