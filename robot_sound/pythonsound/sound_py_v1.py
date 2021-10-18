# import speech_py3
# import os
# import sys
# import string
#
# command1 = {
#     '打开小手': './hand.py',
#     '关闭小手': 'exit ./hand.py',
# }
#
# speech_py3.say('语音识别已开启，工大语音设备助手为您服务')
# while True:
#     phrase = speech_py3.input()
#     print("识别你说的为" + speech_py3.input())
#     # 常用项目
#     if phrase in command1.keys():
#         speech_py3.say('即将为您%s' % phrase)
#         os.system(command1[phrase])
#         speech_py3.say('任务已完成！')
#     # 遥控打开小手程序
#     # if phrase == '打开小手':
#     #     speech_py3.say('5秒后将打开小手')
#     #     time.sleep(5)
#     if phrase == '退出程序':
#         speech_py3.say('已退出程序，感谢使用！')
#         speech_py3.stoplistening()
#         sys.exit()

import speech
import os
import sys

command1 = {
    '打开小手': './hand.py',
    '关闭小手': 'exit ./hand.py',
}

speech.say('语音识别已开启，工大语音设备助手为您服务')
while True:
    phrase = speech.input()
    print("识别你说的为" + speech.input())
    # 常用项目
    if phrase in command1.keys():
        speech.say('即将为您%s' % phrase)
        os.system(command1[phrase])
        speech.say('任务已完成！')
    # 遥控打开小手程序
    # if phrase == '打开小手':
    #     speech_py3.say('5秒后将打开小手')
    #     time.sleep(5)
    if phrase == '退出程序':
        speech.say('已退出程序，感谢使用！')
        speech.stoplistening()
        sys.exit()
