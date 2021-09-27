##########决策
from playsound import  playsound
import winsound
import time
import claw_control

def judge(claw,gamer):
    ## 判断输赢
    if claw == gamer:  # 平手
        time.sleep(0.5)
        winsound.PlaySound('audio/ping.wav',winsound.SND_FILENAME)
        claw_control.reset()
        # pass

    elif (claw == 1 and gamer == 2) or (claw == 2 and gamer == 3) or (
            claw == 3 and gamer == 1):
        # 机器输了
        time.sleep(0.5)
        winsound.PlaySound('audio/shu.wav',winsound.SND_FILENAME)
        claw_control.reset()
        # pass
    elif (claw == 2 and gamer == 1) or (claw == 3 and gamer == 2) or (
            claw == 1 and gamer == 3):
        # 机器赢了
        time.sleep(0.5)
        winsound.PlaySound('audio/ying.wav',winsound.SND_FILENAME)
        claw_control.reset()
        # pass






