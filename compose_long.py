# -*- coding: UTF-8 -*-
# Python 3.x
import http.client
import urllib.request
import json
import time
import requests
from requests.exceptions import RequestException
import logging
import os
logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    filename='日志.log',
                    filemode='a',
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')


headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}


def request_url(url, name, format):
    response = requests.get(url, headers=headers)
    logging.info('状态码: ' + str(response.status_code))
    print('状态码: ' + str(response.status_code))
    try:
        if response.status_code == 200:
            download_voice(url, name, format)
        return None
    except RequestException:
        return None


def download_voice(url, name, format):
    if not os.path.exists('./audioFiles'):
        os.makedirs('./audioFiles')
    file_path = r'./audioFiles/{}.{}'.format(name, format)
    logging.info('正在下载:' + name + '.{}\n'.format(format))
    urllib.request.urlretrieve(url, file_path)
    logging.info(name + '.{}下载完成!!!!!!!!!'.format(format))


class TtsHeader:
    def __init__(self, appkey, token):
        self.appkey = appkey
        self.token = token
    def tojson(self, e):
        return {'appkey': e.appkey, 'token': e.token}


class TtsContext:
    def __init__(self, device_id):
        self.device_id = device_id
    #将序列化函数定义到类中。
    def tojson(self, e):
        return {'device_id': e.device_id}


class TtsRequest:
    def __init__(self, voice, sample_rate, format, enable_subtitle, text):
        self.voice = voice
        self.sample_rate = sample_rate
        self.format = format
        self.enable_subtitle = enable_subtitle
        self.text = text
    def tojson(self, e):
        return {'voice': e.voice, 'sample_rate': e.sample_rate, 'format': e.format, 'enable_subtitle': e.enable_subtitle, 'text': e.text}


class TtsPayload:
    def __init__(self, enable_notify, notify_url, tts_request):
        self.enable_notify = enable_notify
        self.notify_url = notify_url
        self.tts_request = tts_request
    def tojson(self, e):
        return {'enable_notify': e.enable_notify, 'notify_url': e.notify_url, 'tts_request': e.tts_request.tojson(e.tts_request)}


class TtsBody:
    def __init__(self, tts_header, tts_context, tts_payload):
        self.tts_header = tts_header
        self.tts_context = tts_context
        self.tts_payload = tts_payload
    def tojson(self, e):
        return {'header': e.tts_header.tojson(e.tts_header), 'context': e.tts_context.tojson(e.tts_context), 'payload': e.tts_payload.tojson(e.tts_payload)}


# 根据特定信息轮询检查某个请求在服务端的合成状态，轮询操作非必须，如果设置了回调url，则服务端会在合成完成后主动回调。
def waitLoop4Complete(url, appkey, token, task_id, request_id, file_name, format):
    fullUrl = url + "?appkey=" + appkey + "&task_id=" + task_id + "&token=" + token + "&request_id=" + request_id
    # print("fullUrl=", fullUrl)
    host = {"Host":"nls-gateway.cn-shanghai.aliyuncs.com", "Accept":"*/*", "Connection":"keep-alive",'Content-Type': 'application/json'}
    while True:
        req = urllib.request.Request(url=fullUrl)
        result = urllib.request.urlopen(req).read()
        # print("query result = ", result)
        jsonData = json.loads(result.decode('utf-8'))

        if "error_code" in jsonData and jsonData["error_code"] == 20000000 and "data" in jsonData and (jsonData["data"]["audio_address"] != None):
            # print("Tts Finished! task_id = " + jsonData["data"]["task_id"])
            # print("Tts Finished! audio_address = " + jsonData["data"]["audio_address"])
            audio_url = jsonData["data"]["audio_address"]
            request_url(audio_url, file_name, format)
            break
        else:
            print("Tts Running...")
            time.sleep(3)


# 长文本语音合成restful接口，支持post调用，不支持get请求。发出请求后，可以轮询状态或者等待服务端合成后自动回调（如果设置了回调参数）。
def requestLongTts4Post(tts_body, appkey, token, file_name, format):
    host = 'nls-gateway.cn-shanghai.aliyuncs.com'
    url = 'https://' + host + '/rest/v1/tts/async'
    # 设置HTTP Headers
    http_headers = {'Content-Type': 'application/json'}
    # print('The POST request body content: ' + tts_body)
    conn = http.client.HTTPSConnection(host)
    #conn = http.client.HTTPConnection(host)
    conn.request(method='POST', url=url, body=tts_body, headers=http_headers)
    response = conn.getresponse()
    # print('Response status and response reason:')
    # print(response.status, response.reason)
    contentType = response.getheader('Content-Type')
    # print(contentType)
    body = response.read()
    if response.status == 200:
        jsonData = json.loads(body.decode('utf-8'))
        # print('The request succeed : ', jsonData)
        # print('error_code = ', jsonData['error_code'])
        task_id = jsonData['data']['task_id']
        request_id = jsonData['request_id']
        # print('task_id = ', task_id)
        # print('request_id = ', request_id)
        # 说明：轮询检查服务端的合成状态，轮询操作非必须。如果设置了回调url，则服务端会在合成完成后主动回调。
        waitLoop4Complete(url, appkey, token, task_id, request_id, file_name, format)
        return True
    else:
        print('The request failed: ' + str(body))
        return False


def compose_commercial_long(appkey, token, voice, speech_rate, format, volume, file_name, text):
    # 拼接HTTP Post请求的消息体内容。
    th = TtsHeader(appkey, token)
    tc = TtsContext(file_name)
    # TtsRequest对象内容为：发音人、采样率、语音格式、待合成文本内容。
    tr = TtsRequest(voice, 16000, format, False, text)
    # 是否设置回调url，回调url地址，TtsRequest对象。
    tp = TtsPayload(False, "http://134.com", tr)
    tb = TtsBody(th, tc, tp)
    body = json.dumps(tb, default=tb.tojson)
    return requestLongTts4Post(str(body), appkey, token, file_name, format)


if __name__ == '__main__':
    voice = 'Aixiang'
    appkey = 'VNSQETOK5RRVSeRH'
    token = 'd1856e33bc2d4eeb8486111ead398e26'
    speech_rate = -200
    format = 'mp3'
    volume = 100
    file_name = 'audio'
    text = '''岁月匆匆而过，悄悄回首，我已走进小学生活近六年了，念及往事，不生唏嘘。那人生道路上的无数个第一次就像波涛起伏的海浪，荡漾在我的心头。是那样的亲切1而有熟悉，又是那样的美好而和谐。第一次上台表演的经历就一直使我不能忘怀。那是我在五岁第一次上台时，在上台前，我的心忐忑不安，总是无法调整出好的情绪。开始表演了，强烈的镁光灯直射下来，就像一双犀利的眼睛，盯着我喘不过气来。我就更紧张了。当我看到台下这么多人的目光聚集在我的身上，原来就担心的我一下子忘了自己的动作，傻呆呆的站在幕布旁。那一刹那，我听到的音乐就像奔驰的野马，嗡嗡作响；镁光灯则是一把锋利而尖锐的箭，射进了我的内心深处。好在这时，老师在幕布旁不断地鼓励我，小声地说：“你一定能行！”我深深的吸了一口气，很快镇静下来。我微笑着自信地走上了舞台。一上台，我就好像置于一池碧水中，身体变得那样的舒展，跳的每一个动作都是那么娴熟而自然。那音乐如潺潺的溪水，镁光灯也如正午的暖阳。我的舞姿犹如一只傲气的白天鹅在湖面上游动；又像一缕纯洁的阳光，干净而温暖；更像一直蓬勃的向日葵，正努力地向上生长。终于，我在观众们的掌声中退了场。事后，我一直在想：有自信不一定能成功。但是，如果你充满自信，就有成功的希望。自信是飞向蓝天的翅膀，是航行的船桨。在任何时候，自信都会助你一臂之力，助你到达成功的彼岸。让自己成为一个充满自信的人吧！我爱第一次，他教会了我成功的秘笈：充满自信，挑战自信。'''

    compose_commercial_long(appkey, token, voice, speech_rate, format, volume, file_name, text)