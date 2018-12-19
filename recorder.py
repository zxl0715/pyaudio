# -*- coding: utf-8 -*-
"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) YEAR by zxl0715.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
# !usr/bin/env python
# coding=utf-8

# import numpy as np
from pyaudio import PyAudio, paInt16
from datetime import datetime
import wave
# from tkinter import *

# define of params
NUM_SAMPLES = 2000
framerate = 8000
channels = 1
sampwidth = 2
# the longest record time
TIME = 30  # 最长录制时间

FILENAME = ''  # 录制文件名
NOW = ''  # 存储录制时间
SAVE = ''
JUDGE = True  # 进行录制结束的判断


def save_wave_file(filename, data):
    '''save the date to the wav file'''
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes("".join(data))
    wf.close()


def record_wave():
    # open the input of wave
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=1, rate=framerate, input=True, frames_per_buffer=NUM_SAMPLES)
    save_buffer = []
    count = 0
    global JUDGE
    while JUDGE and count < TIME * 4:
        # read NUM_SAMPLES sampling data
        string_audio_data = stream.read(NUM_SAMPLES)
        save_buffer.append(string_audio_data)
        count += 1
        print(".")

    now = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    filename = now + ".wav"
    SAVE = save_wave_file(filename, save_buffer)
    save_buffer = []
    print(filename, "saved")
    global FILENAME, NOW, JUDGE
    FILENAME = filename
    NOW = now


if __name__ == '__main__':
    """先调用recorder中的函数record_wave，然后在录制结束时将recorder中的全局变量JUDGE置为False，即可完成录制。
    """
    record_wave()
