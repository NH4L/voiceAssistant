# -*- coding: utf-8 -*-
import threading
import ali_speech
from ali_speech.callbacks import SpeechSynthesizerCallback
from ali_speech.constant import TTSFormat
from ali_speech.constant import TTSSampleRate

class MyCallback(SpeechSynthesizerCallback):
    # 参数name用于指定保存音频的文件
    def __init__(self, name):
        self._name = name
        self._fout = open(name, 'wb')
    def on_binary_data_received(self, raw):
        print('MyCallback.on_binary_data_received: %s' % len(raw))
        self._fout.write(raw)
    def on_completed(self, message):
        print('MyCallback.OnRecognitionCompleted: %s' % message)
        self._fout.close()
    def on_task_failed(self, message):
        print('MyCallback.OnRecognitionTaskFailed-task_id:%s, status_text:%s' % (
            message['header']['task_id'], message['header']['status_text']))
        self._fout.close()
    def on_channel_closed(self):
        print('MyCallback.OnRecognitionChannelClosed')


def process(client, appkey, token, text, audio_name, voice):
    callback = MyCallback(audio_name)
    synthesizer = client.create_synthesizer(callback)
    synthesizer.set_appkey(appkey)
    synthesizer.set_token(token)
    synthesizer.set_voice(voice)
    synthesizer.set_text(text)
    synthesizer.set_format(TTSFormat.WAV)
    synthesizer.set_sample_rate(TTSSampleRate.SAMPLE_RATE_16K)
    synthesizer.set_volume(50)
    synthesizer.set_speech_rate(-200)
    synthesizer.set_pitch_rate(0)
    try:
        ret = synthesizer.start()
        if ret < 0:
            return ret
        synthesizer.wait_completed()
    except Exception as e:
        print(e)
    finally:
        synthesizer.close()

def process_multithread(client, appkey, token, number):
    thread_list = []
    for i in range(0, number):
        text = "这是线程" + str(i) + "的合成。"
        audio_name = "sy_audio_" + str(i) + ".wav"
        thread = threading.Thread(target=process, args=(client, appkey, token, text, audio_name, voice))
        thread_list.append(thread)
        thread.start()
    for thread in thread_list:
        thread.join()


if __name__ == "__main__":
    client = ali_speech.NlsClient()
    # 设置输出日志信息的级别：DEBUG、INFO、WARNING、ERROR
    client.set_log_level('INFO')
    voice = 'Aixia'
    appkey = 'VNSQETOK5RRVSeRH'
    token = 'f2852ddf530e4105bd5f784f77aade6d'
    text = "岁月匆匆而过，悄悄回首，我已走进小学生活近六年了，念及往事，不生唏嘘。那人生道路上的无数个第一次就像波涛起伏的海浪，荡漾在我的心头。是那样的亲切而有熟悉，又是那样的美好而和谐。第一次上台表演的经历就一直使我不能忘怀。那是我在五岁第一次上台时，在上台前，我的心忐忑不安，总是无法调整出好的情绪。开始表演了，强烈的镁光灯直射下来，就像一双犀利的眼睛，盯着我喘不过气来。我就更紧张了。当我看到台下这么多人的目光聚集在我的身上，原来就担心的我一下子忘了自己的动作，傻呆呆的站在幕布旁。那一刹那，我听到的音乐就像奔驰的野马，嗡嗡作响；镁光灯则是一把锋利而尖锐的箭，射进了我的内心深处。好在这时，老师在幕布旁不断地鼓励我，小声地说：“你一定能行！”我深深的吸了一口气，很快镇静下来。我微笑着自信地走上了舞台。一上台，我就好像置于一池碧水中，身体变得那样的舒展，跳的每一个动作都是那么娴熟而自然。那音乐如潺潺的溪水，镁光灯也如正午的暖阳。我的舞姿犹如一只傲气的白天鹅在湖面上游动；又像一缕纯洁的阳光，干净而温暖；更像一直蓬勃的向日葵，正努力地向上生长。终于，我在观众们的掌声中退了场。事后，我一直在想：有自信不一定能成功。但是，如果你充满自信，就有成功的希望。自信是飞向蓝天的翅膀，是航行的船桨。在任何时候，自信都会助你一臂之力，助你到达成功的彼岸。让自己成为一个充满自信的人吧！我爱第一次，他教会了我成功的秘笈：充满自信，挑战自信。"
    audio_name = 'audio.mp3'
    process(client, appkey, token, text, audio_name, voice)
    # 多线程示例
    # process_multithread(client, appkey, token, 2)