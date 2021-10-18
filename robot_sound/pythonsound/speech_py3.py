"""
Classes:
    Listener: represents a command to execute when phrases are heard.
Functions:
    say(phrase): Say the given phrase out loud.
    input(prompt, phraselist): Block until input heard, then return text.
    stoplistening(): Like calling stoplistening() on all Listeners.
    islistening(): True if any Listener is listening.
    listenforanything(callback): Run a callback when any text is heard.
    listenfor(phraselist, callback): Run a callback when certain text is heard.

Very simple usage example://调用实例

import speech

speech.say("Say something.")

print "You said " + speech.input()

def L1callback(phrase, listener):
    print phrase

def L2callback(phrase, listener):
    if phrase == "关闭监听":
        listener.stoplistening()
    speech.say(phrase)

# 回调在单独的事件线程上执行。
L1 = speech.listenfor(["hello", "good bye"], L1callback)
L2 = speech.listenforanything(L2callback)

assert speech.islistening()
assert L2.islistening()

L1.stoplistening()
assert not L1.islistening()

speech.stoplistening()
"""

from win32com.client import constants as _constants
import win32com.client
import pythoncom
import time
import threading

from win32com.client import gencache
gencache.EnsureModule('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 0, 5, 0)

_voice = win32com.client.Dispatch("SAPI.SpVoice")
_recognizer = win32com.client.Dispatch("SAPI.SpSharedRecognizer")
_listeners = []
_handlerqueue = []
_eventthread=None

#
# class T(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#
#     def run(self):
#             pass
# def _ensure_event_thread(self):
#         """
#         确保事件线程正在运行，这将检查处理程序队列以便创建新的事件处理程序，并运行消息泵。
#         """
#         global _eventthread
#         if not _eventthread:
#             def loop():
#                 while _eventthread:
#                     pythoncom.PumpWaitingMessages()
#                     if _handlerqueue:
#                         (context,listener,callback) = _handlerqueue.pop()
#                         # Just creating a _ListenerCallback object makes events
#                         # fire till listener loses reference to its grammar object
#                         _ListenerCallback(context, listener, callback)
#                     time.sleep(.5)
#             _eventthread = T()
#             _eventthread.start()


class Listener(object):

    """侦听语音并在单独的线程上调用回调."""

    _all = set()

    def __init__(self, context, grammar, callback):
        """
        永远不要直接调用这个函数;使用speech.listenfor ()和speech.listenforanything()来创建Listener对象。
        """
        self._grammar = grammar
        Listener._all.add(self)
        # 告诉事件线程创建一个事件处理程序来调用我们的回调

        # 在听到言语事件时
        _handlerqueue.append((context, self, callback))
        _ensure_event_thread()

    def islistening(self):
        """如果是在听，则为真."""
        return self in Listener._all

    def stoplistening(self):
        """停止监听。如果我们在监听，则返回True."""

        try:
            Listener._all.remove(self)
        except KeyError:
            return False

        # 删除所有指向_grammar的引用，这样事件处理程序就会死亡
        self._grammar = None

        if not Listener._all:
            global _eventthread
            _eventthread = None
            # 如果事件线程存在，则停止它

        return True

_ListenerBase = win32com.client.getevents("SAPI.SpSharedRecoContext")
class _ListenerCallback(_ListenerBase):

    """用于在语音识别时触发事件。这个实例类在其侦听器丢失时自动死亡。
    我们可能需要调用self.close()来释放COM对象，我们应该让goaway()成为self的方法。
    """

    def __init__(self, oobj, listener, callback):
        _ListenerBase.__init__(self, oobj)
        self._listener = listener
        self._callback = callback

    def OnRecognition(self, _1, _2, _3, Result):
        # 当我们的听众停止听的时候，它就会终止
        # object. COM可能正在运行，我们可能需要调用close()
        # 在这之前实例类对象可能死亡
        if self._listener and not self._listener.islistening():
            self.close()
            self._listener = None

        if self._callback and self._listener:
            newResult = win32com.client.Dispatch(Result)
            phrase = newResult.PhraseInfo.GetText()
            self._callback(phrase, self._listener)

def say(phrase):
    """监听程序说出收到的phrase"""
    _voice.Speak(phrase)


def input(prompt: object = None, phraselist: object = None) -> object:
    """
    如果提示符不是None，则打印提示符，然后侦听短语列表中的字符串(或者任何东西，如果phraselist是None的话。)
    返回字符串响应听到的消息。
    注意，这将阻塞线程，直到听到响应或按下ctrl - c。
    :rtype: object
    """
    def response(phrase, listener):
        if not hasattr(listener, '_phrase'):
            listener._phrase = phrase # so outside caller can find it
        listener.stoplistening()

    if prompt:
        print(prompt)

    if phraselist:
        listener = listenfor(phraselist, response)
    else:
        listener = listenforanything(response)

    while listener.islistening():
        time.sleep(.1)

    return listener._phrase # hacky way to pass back a response...

def stoplistening():
    """
    Cause all Listeners to stop listening.  Returns True if at least one
    Listener was listening.
    """
    listeners = set(Listener._all) # clone so stoplistening can pop()
    returns = [l.stoplistening() for l in listeners]
    return any(returns) # was at least one listening?

def islistening():
    """True if any Listeners are listening."""
    return not not Listener._all

def listenforanything(callback):
    """
当听到任何类似语音的声音时，回调(spoken_text, listener)是执行。返回一个Listener对象。
callback的第一个参数将是听到的文本字符串。第二个参数将是返回的同一个监听器对象
listenforanything()。执行发生在一个由所有侦听器回调共享的线程上。
    """
    return _startlistening(None, callback)

def listenfor(phraselist, callback):
    """
如果听到列表中的任何一个短语，Callback (spoken_text, listener)被执行。返回一个Listener对象。
callback的第一个参数将是听到的文本字符串。第二个参数将是返回的同一个监听器对象
listenfor()。执行发生在一个由所有侦听器回调共享的线程上。
    """
    return _startlistening(phraselist, callback)

def _startlistening(phraselist, callback):
    """
在命令和控制模式下开始监听，如果phraselist不是None，如果phraselist为None则为听写模式。当一个短语Heard, callback(phrase_text, listener)被执行。返回一个侦听器对象。
callback的第一个参数将是听到的文本字符串。第二个参数将是返回的同一个监听器对象
listenfor()。执行发生在一个由所有侦听器回调共享的线程上。
    """
    # Make a command-and-control grammar        
    context = _recognizer.CreateRecoContext()
    grammar = context.CreateGrammar()

    if phraselist:
        grammar.DictationSetState(0)
        # dunno why we pass the constants that we do here
        rule = grammar.Rules.Add("rule",
                _constants.SRATopLevel + _constants.SRADynamic, 0)
        rule.Clear()

        for phrase in phraselist:
            rule.InitialState.AddWordTransition(None, phrase)

        # not sure if this is needed - was here before but dupe is below
        grammar.Rules.Commit()

        # Commit the changes to the grammar
        grammar.CmdSetRuleState("rule", 1) # active
        grammar.Rules.Commit()
    else:
        grammar.DictationSetState(1)

    return Listener(context, grammar, callback)

def _ensure_event_thread():
    """
    Make sure the eventthread is running, which checks the handlerqueue
    for new eventhandlers to create, and runs the message pump.
    """
    global _event_thread
    if not _event_thread:
        def loop():
            while _event_thread:
                pythoncom.PumpWaitingMessages()
                if _handlerqueue:
                    (context,listener,callback) = _handlerqueue.pop()
                    # Just creating a _ListenerCallback object makes events
                    # fire till listener loses reference to its grammar object
                    _ListenerCallback(context, listener, callback)
                time.sleep(.5)
        _event_thread = 1
        # so loop doesn't terminate immediately
        _event_thread = threading.start_new_thread(loop, ())

