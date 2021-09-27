from aip import AipSpeech
from playsound import playsound
import winsound
# """ 你的 APPID AK SK """
# APP_ID = '24844252'
# API_KEY = 'kbwIlEAGwyCErpCW3hnKMQw3'
# SECRET_KEY = 'xGEiGLDOMT2Hv9Snr3GSGMF0UcGsogkC'
#
# client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

#computer = client.synthesis('玩的真开心下次再来吧', 'zh', 1, {'vol': 5,'per':4,'spd':5})
# computer = client.synthesis('呜呜呜，你好厉害，我输了', 'zh', 1, {'vol': 5,'per':4,'spd':5})
# computer = client.synthesis('哈哈哈，我赢了', 'zh', 1, {'vol': 5,'per':4,'spd':5})
# computer = client.synthesis('你好呀，我是你们的猜拳机器人，下面我们一起猜拳吧', 'zh', '1', {'vol': 5,'per':4,'spd':5})
# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
winsound.PlaySound('audio/ping.wav',winsound.SND_FILENAME)
# playsound('audio.mp3')
