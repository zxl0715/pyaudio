# -*- coding: utf-8 -*-
"""
    package.module 录音
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) YEAR by zxl0715.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
from configHandler import *
import wave
import pyaudio
import time
import os
from space_size import *

import loggingHandler

# 定义数据流块
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
# 录音时间 单位秒
RECORD_SECONDS = 60
# 要写入的文件名
WAVE_OUTPUT_FILENAME = "new_output.wav"


def recorder(WAVE_OUTPUT_FILENAME):
    # 创建PyAudio对象
    p = pyaudio.PyAudio()
    # 打开数据流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    # 开始录音
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    # 停止数据流
    stream.stop_stream()
    stream.close()

    # 关闭PyAudio
    p.terminate()

    # 写入录音文件
    file_size = p.get_sample_size(FORMAT)
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(file_size)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return file_size


if __name__ == '__main__':
    loggingHandler.logger.info('开始我的 “秘密计划”。')

    runing = True
    run_num = 0
    RECORD_SECONDS = get_record_seconds()
    loggingHandler.logger.info('单个录Y长度为{}秒 ！'.format(RECORD_SECONDS))

    disk_size = get_disk_size()
    disk_path = os.getcwd()[0:3]  # 'C:\\'
    free_space_size = get_free_space_mb(disk_path)  # 单位为'GB'
    loggingHandler.logger.info('路径{}的磁盘空间剩余为 {} GB ，计划剩余为{}GB ！'.format(disk_path, free_space_size, disk_size))

    while runing:
        save_path = './recorder/{}'.format(time.strftime('%Y%m%d', time.localtime(time.time())))
        if os.path.exists(save_path) is False:
            os.mkdir(save_path)

        WAVE_OUTPUT_FILENAME = os.path.join(save_path, 'new_output_{}.wav'.format(
            time.strftime('%Y-%m-%d %H%M%S', time.localtime(time.time()))
        ))
        print(WAVE_OUTPUT_FILENAME)
        loggingHandler.logger.info('录Y中…… ，将生成 {} 文件！'.format(WAVE_OUTPUT_FILENAME))

        file_size = recorder(WAVE_OUTPUT_FILENAME)
        loggingHandler.logger.info('录Y完成生成 {} 文件。'.format(WAVE_OUTPUT_FILENAME))

        # run_num = run_num + 1
        # if run_num > 10:
        #     # 录音10次后判断磁盘空间
        #     run_num = 0
        free_space_size = get_free_space_mb(disk_path)  # 单位为'GB'
        if free_space_size < disk_size:
            loggingHandler.logger.warning(
                '路径{}的磁盘空间剩余为 {} GB ，计划剩余为{}GB ！'.format(disk_path, free_space_size, disk_size))
            file_list = get_file_list(save_path)
            for list_count in len(file_list):
                os.remove(os.path.join(save_path, file_list[0]))
                loggingHandler.logger.info('删除文件：{}成功信息！'.format(os.path.join(save_path, file_list[0])))

            print(file_list)
