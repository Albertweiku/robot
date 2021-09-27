################################
######
##创建多线程：手势识别线程、语音识别线程
######
################################
import threading
import time

import claw_control
import hand
import random
from playsound import playsound
from claw_control import punch
import judge
import winsound
import globalvar as gl
import speech_recognition

def control():
    claw_control.start_hand()

def speak_start():
    winsound.PlaySound('audio/start.wav', winsound.SND_FILENAME)

##手势线程
def hand_thread():
    # global recognition
    time.sleep(0.1)
    hand.detect(recognition)

##语音线程和总线程的集合
def speech_recognition_thread():
    global recognition, first

    result = speech_recognition.song2text()

    # result = '你好'
    if result == '你好':
    # if True:
        #手势识别线程
        if  first == True:
            hand1 = threading.Thread(target=hand_thread)
            hand1.setDaemon(True)
            hand1.start()

            handStart = threading.Thread(target=control())
            speakStart = threading.Thread(target=speak_start())

            handStart.start()
            speakStart.start()


            # ##欢迎语音回馈
            # winsound.PlaySound('audio/start.wav',winsound.SND_FILENAME)

        # result = speech_recognition.song2text()
        result = True
        # result = '好的'
        while(True):
            if (result) or (first == False):
            # if True:

                winsound.PlaySound("audio/kouling.wav", winsound.SND_FILENAME)
                claw = punch()
                print("claw")
                print(claw)
                time.sleep(0.5)
                recognition = True  # 控制手势线程识别
                gamer = hand.send_gamer()
                first = False
                if gamer == 0:
                    winsound.PlaySound("audio/no.wav", winsound.SND_FILENAME)
                    claw_control.reset()
                    recognition = False
                    gamer = 0
                    # time.sleep(1)
                else:

                    # print(type(gamer))
                    if recognition == False:
                        gamer = 0
                    judge.judge(claw, gamer)
                    time.sleep(1)
                    gamer = 0
                    recognition = False
                ###判断程序是否继续
                # winsound.PlaySound('audio/ask.wav', winsound.SND_FILENAME)
                recognition = False
                result = speech_recognition.song2text()
                # result = '好的'
                first = False
                gamer = 0
                if result == "不玩了":
                # if True:
                    winsound.PlaySound('audio/end.wav',winsound.SND_FILENAME)
                    claw_control.reset()
                    return
                ###################################3
                # ##添加逻辑判断，避免线程过多
                # elif result == "好的":
                #     winsound.PlaySound('audio/restart.wav', winsound.SND_FILENAME)
                #     first = False
                #     # speech_recognition_thread()
                # else:
                #     return
            else:
                recognition = False
                return
    else:
        print("没有识别到你说的话！")

def send_recognition():
    return recognition

if __name__ == '__main__':
    first = True #是否为第一次
    recognition = False #识别控制
    speech = threading.Thread(target=speech_recognition_thread) #把子进程设置为守护线程，必须在start()之前设置
    speech.start()
    print('end')

recognition = True













