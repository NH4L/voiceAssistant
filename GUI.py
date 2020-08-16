# coding:utf-8
import threading
import os
from PyQt5 import QtCore,QtGui,QtWidgets
import sys
import qtawesome
from PyQt5.QtGui import QCursor, QDesktopServices, QIcon
from PyQt5.QtCore import Qt, QUrl
import webbrowser
import re
from voiceComposeByUrl import compose
import logging
import datetime
import json
from PyQt5.QtCore import QThread, pyqtSignal
from functools import partial

logging.basicConfig(
    level=logging.DEBUG,#控制台打印的日志级别
    filename='日志.log',
    filemode='a',
    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
)


voice_json = {
    "小云": "Xiaoyun",
    "小刚": "Xiaogang",
    "若兮": "Ruoxi",
    "思琪": "Siqi",
    "思佳": "Sijia",
    "思诚": "Sicheng",
    "艾琪": "Aiqi",
    "艾佳": "Aijia",
    "艾诚": "Aicheng",
    "艾达": "Aida",
    "宁儿": "Ninger",
    "瑞琳": "Ruilin",
    "思悦": "Siyue",
    "艾雅": "Aiya",
    "艾夏": "Aixia",
    "艾美": "Aimei",
    "艾雨": "Aiyu",
    "艾悦": "Aiyue",
    "艾婧": "Aijing",
    "小美": "Xiaomei",
    "艾娜": "Aina",
    "伊娜": "Yina",
    "思婧": "Sijing",
    "思彤": "Sitong",
    "小北": "Xiaobei",
    "艾彤": "Aitong",
    "艾薇": "Aiwei",
    "艾宝": "Aibao",
    "姗姗": "Shanshan",
    "小玥": "Xiaoyue",
    "Lydia": "Lydia",
    "艾硕": "Aishuo",
    "青青": "Qingqing",
    "翠姐": "Cuijie",
    "小泽": "Xiaoze"
}


class message(QThread):
    signal = pyqtSignal()

    def __init__(self, Window):
        super(message, self).__init__()
        self.window = Window

    def run(self):
        self.signal.emit()


class MainUi(QtWidgets.QMainWindow):
    __dragWin = True
    def __init__(self):
        super().__init__()
        QtWidgets.QMainWindow.__init__(self, windowTitle="配音助手")
        QtWidgets.QMainWindow.setWindowIcon(self, QIcon('./assets/voiceAssistant.jpg'))
        self.__dragWin = False
        self.init_ui()

    def mousePressEvent(self, e):
        self.__dragWin = True
        self.__dragWin_x = e.x()
        self.__dragWin_y = e.y()
        self.setCursor(QCursor(Qt.OpenHandCursor))         # 更改鼠标图标

    def mouseMoveEvent(self, e):
        if self.__dragWin == True:
            pos = e.globalPos()
            length = pos.y() - self.__dragWin_y
            width = pos.x() - self.__dragWin_x
            self.move(width, length)

    def mouseReleaseEvent(self, e):
        self.__dragWin = False
        self.setCursor(QCursor(Qt.ArrowCursor))         # 还原鼠标图标

    def pushButton_show_max_normal(self):
        if MainUi.isMaximized(self):
            self.showNormal()
        else:
            self.showMaximized()

    def print_value(self, select_value):
        return select_value

    def get_now_time(self):
        now = datetime.datetime.now()
        time = 'AUDIO_' + str(now.year) + str(now.month) + str(now.day) + '_' \
               + str(now.hour) + str(now.minute) + str(now.second) + '_'
        return time

    def open_test_voice_url(self):
        try:
            webbrowser.open('https://ai.aliyun.com/nls/tts')
        except Exception as e:
            webbrowser.open_new_tab('https://ai.aliyun.com/nls/tts')


    def check_format(self, str, type):
        if str != '':
            reg = re.compile(r'^-?[1-9]+[0-9]*$')  # 定义正则表达式
            result = reg.match(str)
            if result:
                result = int(str)
                if 'speech_rate' == type:
                    if result >= -500 and result <= 500:
                        return 'success'
                    else:
                        return '请输入范围中整数！'
                if 'volume' == type:
                    if result >= 0 and result <= 100:
                        return 'success'
                    else:
                        return '请输入范围中整数！'

            else:
                return '请输入整数！'
        else:
            if 'speech_rate' == type:
                    return '语音速率不能为空！'
            if 'volume' == type:
                    return '音量不能为空！'


    def compose_voice_(self, appkey, token, voice, speech_rate, format, volume, file_name, text):
        res = compose(appkey, token, voice, speech_rate, format, volume, file_name, text)
        logging.info(res)
        if res == 'network fail':
            self.message = message(self)
            self.message.signal.connect(partial(self.warning_box_kong, '未连接网络，请连接后重试'))
            self.message.start()
            logging.warning('网络未连接')
        elif res == 'token expired':
            self.message = message(self)
            self.message.signal.connect(partial(self.warning_box_kong, 'token过期,请重新到阿里云粘贴token后充重试'))
            self.message.start()
            logging.warning('token过期')
        elif res == 'success':
            self.message = message(self)
            self.message.signal.connect(partial(self.warning_box_kong, '音频合成成功'))
            self.message.start()
            logging.info('音频合成成功')



    def start_compose(self):
        # 创建线程
        self.thread = threading.Thread(target=self.compose)
        # 开始线程
        self.thread.start()


    def warning_box(self, text):
        QtWidgets.QMessageBox.warning(self, 'Warning', "未填写{0}！".format(text))

    def warning_box_kong(self, text):
        QtWidgets.QMessageBox.warning(self, 'Warning', "{0}！".format(text))


    def compose(self):
        self.compose_voice_button.setEnabled(False)

        appkey = self.right_bar_widget_appkey_input.text()
        if appkey != '':
            token = self.right_bar_widget_token_input.text()
            if token != '':
                speech_rate = self.right_bar_widget_speech_rate_input.text()
                result_speech_rate = self.check_format(speech_rate, 'speech_rate')
                if result_speech_rate == 'success':
                    speech_rate = int(speech_rate)
                    volume = self.right_bar_widget_volume_input.text()
                    result_volume = self.check_format(volume, 'volume')
                    if result_volume == 'success':
                        volume = int(volume)
                        file_name = self.get_now_time()
                        text = self.right_bar_widget_text_input.toPlainText()
                        if len(text) > 0:
                            format = self.right_bar_widget_format_input.currentText()
                            voice = self.right_bar_widget_voice_input.currentText()
                            logging.info('appkey = ' + appkey)
                            logging.info('token = ' + token)
                            logging.info('speech_rate = ' + str(speech_rate))
                            logging.info('volume = ' + str(volume))
                            logging.info('file_name = ' + file_name)
                            logging.info('text = ' + text)
                            logging.info('format = ' + format)
                            logging.info('voice = ' + voice + '__' + voice_json[voice])
                            logging.info('参数填写完毕')
                            self.write_voice_info_json(appkey, token, speech_rate, volume, format, voice)
                            logging.info('写入json文件信息成功')
                            self.compose_voice_(appkey, token, voice_json[voice], speech_rate, format, volume, file_name, text)
                        else:
                            self.message = message(self)
                            self.message.signal.connect(partial(self.warning_box, '文本'))
                            self.message.start()

                    else:
                        self.message = message(self)
                        self.message.signal.connect(partial(self.warning_box_kong, result_volume))
                        self.message.start()
                else:
                    self.message = message(self)
                    self.message.signal.connect(partial(self.warning_box_kong, result_speech_rate))
                    self.message.start()
            else:
                self.message = message(self)
                self.message.signal.connect(partial(self.warning_box, 'token'))
                self.message.start()
        else:
            self.message = message(self)
            self.message.signal.connect(partial(self.warning_box, 'appkey'))
            self.message.start()
        self.compose_voice_button.setEnabled(True)


    def push_button_compose_clicked(self):
        self.right_widget.setVisible(True)
        self.right_widget_shuoming.setVisible(False)
        self.right_widget_xiazai.setVisible(False)
        self.right_widget_fankui.setVisible(False)
        self.right_widget_guanyu.setVisible(False)
        self.right_widget_wenti.setVisible(False)


    def push_button_shuoming_clicked(self):
        self.right_widget.setVisible(False)
        self.right_widget_shuoming.setVisible(True)
        self.right_widget_xiazai.setVisible(False)
        self.right_widget_fankui.setVisible(False)
        self.right_widget_guanyu.setVisible(False)
        self.right_widget_wenti.setVisible(False)


    def push_button_xiazai_clicked(self):
        self.right_widget.setVisible(False)
        self.right_widget_shuoming.setVisible(False)
        self.right_widget_xiazai.setVisible(True)
        self.right_widget_fankui.setVisible(False)
        self.right_widget_guanyu.setVisible(False)
        self.right_widget_wenti.setVisible(False)


    def push_button_fankui_clicked(self):
        self.right_widget.setVisible(False)
        self.right_widget_shuoming.setVisible(False)
        self.right_widget_xiazai.setVisible(False)
        self.right_widget_fankui.setVisible(True)
        self.right_widget_guanyu.setVisible(False)
        self.right_widget_wenti.setVisible(False)


    def push_button_guanyu_clicked(self):
        self.right_widget.setVisible(False)
        self.right_widget_shuoming.setVisible(False)
        self.right_widget_xiazai.setVisible(False)
        self.right_widget_fankui.setVisible(False)
        self.right_widget_guanyu.setVisible(True)
        self.right_widget_wenti.setVisible(False)


    def push_button_wenti_clicked(self):
        self.right_widget.setVisible(False)
        self.right_widget_shuoming.setVisible(False)
        self.right_widget_xiazai.setVisible(False)
        self.right_widget_fankui.setVisible(False)
        self.right_widget_guanyu.setVisible(False)
        self.right_widget_wenti.setVisible(True)


    def open_xaizai_file(self):
        if not os.path.exists('./audioFiles'):
            os.makedirs('./audioFiles')
        QDesktopServices.openUrl(QUrl('file:///' + os.getcwd() + '/audioFiles'))


    def get_last_voice_info(self):
        if not os.path.exists('./voice_data.json'):
            logging.info('首次进行语音合成无json信息文件')
        else:
            data = json.load(open("./voice_data.json"))
            appkey = data['appkey']
            self.right_bar_widget_appkey_input.setText(appkey)
            token = data['token']
            self.right_bar_widget_token_input.setText(token)
            speech_rate = data['speech_rate']
            self.right_bar_widget_speech_rate_input.setText(str(speech_rate))
            volume = data['volume']
            self.right_bar_widget_volume_input.setText(str(volume))
            format = data['format']
            self.right_bar_widget_format_input.setCurrentText(format)
            voice = data['voice']
            self.right_bar_widget_voice_input.setCurrentText(voice)

            logging.info('读取json语音合成历史信息成功')


    def write_voice_info_json(self, appkey, token, speech_rate, volume, format, voice):
        compose_info = {}
        data = json.loads(json.dumps(compose_info))
        data['appkey'] = appkey
        data['token'] = token
        data['speech_rate'] = speech_rate
        data['volume'] = volume
        data['format'] = format
        data['voice'] = voice
        compose_info = json.dumps(data, indent=4, ensure_ascii=False)

        # print(compose_info)
        with open('./voice_data.json', 'w') as json_file:
            json_file.write(compose_info)


    def init_ui(self):
        self.setFixedSize(960,700)

        self.main_widget = QtWidgets.QWidget() # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout() # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout) # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget() # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout() # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget,0,0,12,2) # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget,0,2,12,10) # 右侧部件在第0行第3列，占8行9列

        self.left_close = QtWidgets.QPushButton("", self)  # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("", self)  # 最大化按钮
        self.left_mini = QtWidgets.QPushButton("", self)  # 最小化按钮
        self.left_close.setToolTip('关闭')

        self.left_visit.setToolTip('最大化')
        self.left_visit.clicked.connect(self.pushButton_show_max_normal)  # 点击按钮之后最大化窗口

        self.left_mini.setToolTip('最小化')
        self.left_close.clicked.connect(self.close)  # 点击按钮之后关闭窗口
        self.left_mini.clicked.connect(self.showMinimized)  # 点击按钮之后最小化窗口

        self.left_label_1 = QtWidgets.QPushButton("配音助手")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("联系与帮助")
        self.left_label_2.setObjectName('left_label')

        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.cog', color='white'), "语音合成")
        self.left_button_1.setObjectName('left_button')
        self.left_button_1.clicked.connect(self.push_button_compose_clicked)
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.hand-o-right', color='white'), "使用说明")
        self.left_button_2.setObjectName('left_button')
        self.left_button_2.clicked.connect(self.push_button_shuoming_clicked)
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.download', color='white'), "下载管理")
        self.left_button_3.setObjectName('left_button')
        self.left_button_3.clicked.connect(self.push_button_xiazai_clicked)
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.comment', color='white'), "反馈建议")
        self.left_button_4.setObjectName('left_button')
        self.left_button_4.clicked.connect(self.push_button_fankui_clicked)
        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "关于我们")
        self.left_button_5.setObjectName('left_button')
        self.left_button_5.clicked.connect(self.push_button_guanyu_clicked)
        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.question', color='white'), "遇到问题")
        self.left_button_6.setObjectName('left_button')
        self.left_button_6.clicked.connect(self.push_button_wenti_clicked)
        self.left_xxx = QtWidgets.QPushButton(" ")

        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_3, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_4, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_5, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_6, 8, 0, 1, 3)


        self.right_arg_label = QtWidgets.QLabel("参数设置")
        self.right_arg_label.setObjectName('right_lable')
        self.right_layout.addWidget(self.right_arg_label, 0, 0, 1, 9)

        # 第一行appkey和token
        self.right_arg1_widget = QtWidgets.QWidget()  # 第一行参数部件
        self.right_arg1_layout = QtWidgets.QGridLayout()  # 第一行参数网格布局
        self.right_arg1_widget.setLayout(self.right_arg1_layout)
        self.right_arg11_widget = QtWidgets.QWidget()  # 第一行第一个参数部件
        self.right_arg11_layout = QtWidgets.QGridLayout()  # 第一行第一个参数网格布局
        self.right_arg11_widget.setLayout(self.right_arg11_layout)
        self.right_arg12_widget = QtWidgets.QWidget()  # 第一行第二个参数部件
        self.right_arg12_layout = QtWidgets.QGridLayout()  # 第一行第二个参数网格布局
        self.right_arg12_widget.setLayout(self.right_arg12_layout)

        self.appkey_icon = QtWidgets.QLabel('appkey')
        self.appkey_icon.setFont(qtawesome.font('fa', 16))
        self.right_bar_widget_appkey_input = QtWidgets.QLineEdit()
        self.right_bar_widget_appkey_input.setPlaceholderText("输入appkey")

        self.token_icon = QtWidgets.QLabel('token')
        self.token_icon.setFont(qtawesome.font('fa', 16))
        self.right_bar_widget_token_input = QtWidgets.QLineEdit()
        self.right_bar_widget_token_input.setPlaceholderText("输入token")

        self.right_arg11_layout.addWidget(self.appkey_icon, 1, 0, 1, 1)
        self.right_arg11_layout.addWidget(self.right_bar_widget_appkey_input, 1, 1, 1, 3)
        self.right_arg12_layout.addWidget(self.token_icon, 1, 4, 1, 1)
        self.right_arg12_layout.addWidget(self.right_bar_widget_token_input, 1, 5, 1, 3)
        self.right_arg1_layout.addWidget(self.right_arg11_widget, 1, 0, 1, 4)
        self.right_arg1_layout.addWidget(self.right_arg12_widget, 1, 4, 1, 4)

        self.right_layout.addWidget(self.right_arg1_widget, 1, 0, 1, 6)

        # 第二行输入文本text
        self.right_arg2_widget = QtWidgets.QWidget()  # 第二行参数部件
        self.right_arg2_layout = QtWidgets.QGridLayout()  # 第二行参数网格布局
        self.right_arg2_widget.setLayout(self.right_arg2_layout)

        self.text_icon = QtWidgets.QLabel('输入文本')
        self.text_icon.setFont(qtawesome.font('fa', 14))
        self.right_bar_widget_text_input = QtWidgets.QTextEdit()
        self.right_bar_widget_text_input.setPlaceholderText("输入格式请看“使用说明”")

        self.right_arg2_layout.addWidget(self.text_icon, 2, 0, 1, 1)
        self.right_arg2_layout.addWidget(self.right_bar_widget_text_input, 2, 1, 1, 8)
        self.right_layout.addWidget(self.right_arg2_widget, 2, 0, 1, 9)

        # 第三行speech_rate和volume
        self.right_arg3_widget = QtWidgets.QWidget()
        self.right_arg3_layout = QtWidgets.QGridLayout()
        self.right_arg3_widget.setLayout(self.right_arg3_layout)
        self.right_arg31_widget = QtWidgets.QWidget()
        self.right_arg31_layout = QtWidgets.QGridLayout()
        self.right_arg31_widget.setLayout(self.right_arg31_layout)
        self.right_arg32_widget = QtWidgets.QWidget()
        self.right_arg32_layout = QtWidgets.QGridLayout()
        self.right_arg32_widget.setLayout(self.right_arg32_layout)
        self.right_arg33_widget = QtWidgets.QWidget()
        self.right_arg33_layout = QtWidgets.QGridLayout()
        self.right_arg33_widget.setLayout(self.right_arg33_layout)

        self.speech_rate_icon = QtWidgets.QLabel('语音速率')
        self.speech_rate_icon.setFont(qtawesome.font('fa', 16))
        self.right_bar_widget_speech_rate_input = QtWidgets.QLineEdit()
        self.right_bar_widget_speech_rate_input.setPlaceholderText("-500-500(-100中)")
        self.right_bar_widget_speech_rate_input.setText('-100')

        self.format_icon = QtWidgets.QLabel('音频格式')
        self.format_icon.setFont(qtawesome.font('fa', 16))
        self.right_bar_widget_format_input = QtWidgets.QComboBox(self)
        self.right_bar_widget_format_input.addItems(['mp3', 'wav', 'pcm'])

        self.right_bar_widget_format_input.currentIndexChanged[str].connect(self.print_value)  # 条目发生改变，发射信号，传递条目内容
        # self.right_bar_widget_format_input.currentIndexChanged[int].connect(self.print_value)  # 条目发生改变，发射信号，传递条目索引

        self.volume_icon = QtWidgets.QLabel('    音量')
        self.volume_icon.setFont(qtawesome.font('fa', 16))
        self.right_bar_widget_volume_input = QtWidgets.QLineEdit()
        self.right_bar_widget_volume_input.setPlaceholderText("0-100(建议100)")
        self.right_bar_widget_volume_input.setText('100')

        self.right_arg31_layout.addWidget(self.speech_rate_icon, 3, 0, 1, 1)
        self.right_arg31_layout.addWidget(self.right_bar_widget_speech_rate_input, 3, 1, 1, 2)
        self.right_arg32_layout.addWidget(self.format_icon, 3, 3, 1, 1)
        self.right_arg32_layout.addWidget(self.right_bar_widget_format_input, 3, 4, 1, 2)
        self.right_arg33_layout.addWidget(self.volume_icon, 3, 6, 1, 1)
        self.right_arg33_layout.addWidget(self.right_bar_widget_volume_input, 3, 7, 1, 3)
        self.right_arg3_layout.addWidget(self.right_arg31_widget, 3, 0, 1, 3)
        self.right_arg3_layout.addWidget(self.right_arg32_widget, 3, 3, 1, 3)
        self.right_arg3_layout.addWidget(self.right_arg33_widget, 3, 6, 1, 3)
        self.right_layout.addWidget(self.right_arg3_widget, 3, 0, 1, 9)


        # 第四行voice和audio
        self.right_arg4_widget = QtWidgets.QWidget()
        self.right_arg4_layout = QtWidgets.QGridLayout()
        self.right_arg4_widget.setLayout(self.right_arg4_layout)
        self.right_arg41_widget = QtWidgets.QWidget()
        self.right_arg41_layout = QtWidgets.QGridLayout()
        self.right_arg41_widget.setLayout(self.right_arg41_layout)
        self.right_arg42_widget = QtWidgets.QWidget()
        self.right_arg42_layout = QtWidgets.QGridLayout()
        self.right_arg42_widget.setLayout(self.right_arg42_layout)


        self.voice_icon = QtWidgets.QLabel('音色')
        self.voice_icon.setFont(qtawesome.font('fa', 16))
        self.right_bar_widget_voice_input = QtWidgets.QComboBox(self)
        self.right_bar_widget_voice_input.addItems(['艾夏','小云', '小刚', '若兮', '思琪', '思佳', '思诚', '艾琪', '艾佳', '艾诚', '艾达', '宁儿', '瑞琳', '思悦', '艾雅',  '艾美', '艾雨', '艾悦', '艾婧', '小美', '艾娜', '伊娜', '思婧', '思彤', '小北', '艾彤', '艾薇', '艾宝', '姗姗', '小玥', 'Lydia', '艾硕', '青青', '翠姐', '小泽'])
        self.test_voice_button = QtWidgets.QPushButton('配音试听')
        self.test_voice_button.setFont(qtawesome.font('fa', 16))
        self.test_voice_button.clicked.connect(self.open_test_voice_url)
        self.compose_voice_button = QtWidgets.QPushButton('音频合成')
        self.compose_voice_button.setFont(qtawesome.font('fa', 16))
        self.compose_voice_button.clicked.connect(self.start_compose)
        self.right_bar_widget_voice_input.currentIndexChanged[str].connect(self.print_value)  # 条目发生改变，发射信号，传递条目内容
        # self.right_bar_widget_voice_input.currentIndexChanged[int].connect(self.print_value)  # 条目发生改变，发射信号，传递条目索引



        self.right_arg41_layout.addWidget(self.voice_icon, 4, 0, 1, 1)
        self.right_arg41_layout.addWidget(self.right_bar_widget_voice_input, 4, 1, 1, 2)
        self.right_arg42_layout.addWidget(self.test_voice_button, 4, 3, 1, 2)
        self.right_arg42_layout.addWidget(self.compose_voice_button, 4, 5, 1, 2)
        self.right_arg4_layout.addWidget(self.right_arg41_widget, 4, 0, 1, 3)
        self.right_arg4_layout.addWidget(self.right_arg42_widget, 4, 3, 1, 9)
        self.right_layout.addWidget(self.right_arg4_widget, 4, 0, 1, 9)


        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小


        # 说明
        self.right_widget_shuoming = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget_shuoming.setObjectName('right_widget_shuoming')
        self.right_layout_shuoming = QtWidgets.QGridLayout()
        self.right_widget_shuoming.setLayout(self.right_layout_shuoming)  # 设置右侧部件布局为网格
        self.right_widget_shuoming.setVisible(False)

        self.main_layout.addWidget(self.right_widget_shuoming, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.shuoming_text = QtWidgets.QLabel('1、打开网址：<a href="https://zhuanlan.zhihu.com/p/123930042" style="color:blue">https://zhuanlan.zhihu.com/p/123930042</a><br>'
                                              '2、按照文章中提示注册登录阿里云，获得智能语音交互的appkey和token(会过期)<br>'
                                              '3、在语音合成中，输入相应的参数，即可进行语音合成，进行配音<br>'
                                              '4、输入文本中目前支持中文进行配音，且必须有句号等标点符号，<br>      本程序利用句号“。”才进行分割，所以请按规范输入文本<br>'
                                              '5、音色选择可以在点击配音试听，到阿里云官网选择你需要的配音音色<br>'
                                              '6、语音合成的速度：300字符以内（10秒），800字符（25秒左右）,请耐心等待<br>'
                                              '7、当前语音合成并发数为2（免费版最大并发数），普通使用者足够<br>'
                                              '8、合成音频在当前目录audioFiles中,文件名称为"日期.mp3"<br>'
                                              '9、根据字符长度讲每段字符数限制在300内进行合成，若有800字，则可能生成3个音频文件<br>'
                                              '9、目录下会生成日志文件：“日志.log”<br>'
                                              '10、目录下生成音频合成信息文件：“voice_data.json”，记录上次合成信息<br>')
        self.shuoming_text.setObjectName('shuoming_text_lable')
        self.shuoming_text.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.shuoming_text.setOpenExternalLinks(True)
        self.right_layout_shuoming.addWidget(self.shuoming_text, 0, 0, 12, 10)


        self.right_widget_xiazai = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget_xiazai.setObjectName('right_widget_xiazai')
        self.right_layout_xiazai = QtWidgets.QGridLayout()
        self.right_widget_xiazai.setLayout(self.right_layout_xiazai)  # 设置右侧部件布局为网格
        self.right_widget_xiazai.setVisible(False)

        self.main_layout.addWidget(self.right_widget_xiazai, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.xiazai_button = QtWidgets.QPushButton('打开下载文件夹')
        self.xiazai_button.setFont(qtawesome.font('fa', 16))
        self.xiazai_button.clicked.connect(self.open_xaizai_file)
        self.right_layout_xiazai.addWidget(self.xiazai_button, 0, 0, 12, 10)


        self.right_widget_fankui = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget_fankui.setObjectName('right_widget_fankui')
        self.right_layout_fankui = QtWidgets.QGridLayout()
        self.right_widget_fankui.setLayout(self.right_layout_fankui)  # 设置右侧部件布局为网格
        self.right_widget_fankui.setVisible(False)

        self.main_layout.addWidget(self.right_widget_fankui, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.fankui_text = QtWidgets.QLabel('1、发送邮件至 : nh4l@qq.com <br>' +
                                            '2、发送邮件至 : nh4ly@outlook.com<br>' +
                                            '3、知乎 @NH4L私信 : <a href="https://www.zhihu.com/people/NH4L/posts" style="color:blue">https://www.zhihu.com/people/NH4L</a><br>' +
                                            '4、CSDN @NH4L博客私信 : <a href="https://blog.csdn.net/LeeGe666" style="color:blue">https://blog.csdn.net/LeeGe666</a><br>')
        self.fankui_text.setObjectName('fankui_text_lable')
        self.fankui_text.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.fankui_text.setOpenExternalLinks(True)
        self.right_layout_fankui.addWidget(self.fankui_text, 0, 0, 12, 10)


        self.right_widget_guanyu = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget_guanyu.setObjectName('right_widget_guanyu')
        self.right_layout_guanyu = QtWidgets.QGridLayout()
        self.right_widget_guanyu.setLayout(self.right_layout_guanyu)  # 设置右侧部件布局为网格
        self.right_widget_guanyu.setVisible(False)

        self.main_layout.addWidget(self.right_widget_guanyu, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.guanyu_text = QtWidgets.QLabel('1、本人是一位大学生, 计算机科学与技术专业，<br>     对软件开发，机器学习，大数据有较大兴趣；<br>'
                                            '2、如需和我交流 +qq：2283373978<br>'
                                            '                           +微信：nh4lan<br>'
                                            '3、本软件调用阿里云免费语音合成接口，利用阿里云的API薅羊毛，<br>      不读取用户任何信息，请放心使用<br>'
                                            '4、本软件完全开源 github @NH4L  <a href="https://github.com/NH4L/voiceAssistant" style="color:blue">https://github.com/NH4L/voiceAssistant</a> <br>'
                                            '5、我的CSDN博客 @NH4L <a href="https://blog.csdn.net/LeeGe666" style="color:blue">https://blog.csdn.net/LeeGe666</a> <br>'
                                            '                           @Copyright NH4L All Rights Reserved')
        self.guanyu_text.setObjectName('guanyu_text_lable')
        self.guanyu_text.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.guanyu_text.setOpenExternalLinks(True)
        self.right_layout_guanyu.addWidget(self.guanyu_text, 0, 0, 12, 10)

        self.right_widget_wenti = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget_wenti.setObjectName('right_widget_wenti')
        self.right_layout_wenti = QtWidgets.QGridLayout()
        self.right_widget_wenti.setLayout(self.right_layout_wenti)  # 设置右侧部件布局为网格
        self.right_widget_wenti.setVisible(False)

        self.main_layout.addWidget(self.right_widget_wenti, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.wenti_text = QtWidgets.QLabel('1、有问题联系   +qq：2283373978<br>'
                                            '                          +微信：nh4lan<br>'
                                            '2、知乎私信 @NH4L <a href="https://www.zhihu.com/people/NH4L/posts" style="color:blue">https://www.zhihu.com/people/NH4L</a> <br>'
                                            '3、CSDN博客私信 @NH4L <a href="https://blog.csdn.net/LeeGe666" style="color:blue">https://blog.csdn.net/LeeGe666</a> <br>')
        self.wenti_text.setObjectName('wenti_text_lable')
        self.wenti_text.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.wenti_text.setOpenExternalLinks(True)
        self.right_layout_wenti.addWidget(self.wenti_text, 0, 0, 12, 10)


        self.setCentralWidget(self.main_widget) # 设置窗口主部件

        self.get_last_voice_info()


        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677 url(./assets/exit.png) no-repeat;border-radius:5px;}QPushButton:hover{background:red url(./assets/exit.png);}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674 url(./assets/max.png) no-repeat;border-radius:5px;}QPushButton:hover{background:yellow  url(./assets/max.png);}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D url(./assets/min.png) no-repeat;border-radius:5px;}QPushButton:hover{background:green  url(./assets/min.png);}''')

        self.left_widget.setStyleSheet('''
          QPushButton{border:none;color:white;}
          QPushButton#left_label{
            border:none;
            border-bottom:1px solid white;
            font-size:18px;
            font-weight:700;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
          }
          QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
        ''')

        self.right_widget.setStyleSheet('''
          QWidget#right_widget{
            color:#232C51;
            background:white;
            border-top:1px solid darkGray;
            border-bottom:1px solid darkGray;
            border-right:1px solid darkGray;
            border-top-right-radius:10px;
            border-bottom-right-radius:10px;
          }
          QLabel#right_lable{
            border:none;
            font-size:16px;
            font-weight:700;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
          }
        ''')
        self.right_widget_shuoming.setStyleSheet('''
                  QWidget#right_widget_shuoming{
                    color:#232C51;
                    background:white;
                    border-top:1px solid darkGray;
                    border-bottom:1px solid darkGray;
                    border-right:1px solid darkGray;
                    border-top-right-radius:10px;
                    border-bottom-right-radius:10px;
                  }
                  QLabel#shuoming_text_lable{
                    border:none;
                    font-size:16px;
                    font-weight:700;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                  }
                ''')
        self.right_widget_fankui.setStyleSheet('''
                          QWidget#right_widget_fankui{
                            color:#232C51;
                            background:white;
                            border-top:1px solid darkGray;
                            border-bottom:1px solid darkGray;
                            border-right:1px solid darkGray;
                            border-top-right-radius:10px;
                            border-bottom-right-radius:10px;
                          }
                          QLabel#fankui_text_lable{
                            border:none;
                            font-size:16px;
                            font-weight:700;
                            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                          }
                        ''')
        self.right_widget_guanyu.setStyleSheet('''
                                  QWidget#right_widget_guanyu{
                                    color:#232C51;
                                    background:white;
                                    border-top:1px solid darkGray;
                                    border-bottom:1px solid darkGray;
                                    border-right:1px solid darkGray;
                                    border-top-right-radius:10px;
                                    border-bottom-right-radius:10px;
                                  }
                                  QLabel#guanyu_text_lable{
                                    border:none;
                                    font-size:16px;
                                    font-weight:700;
                                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                                  }
                                ''')
        self.right_widget_wenti.setStyleSheet('''
                                          QWidget#right_widget_wenti{
                                            color:#232C51;
                                            background:white;
                                            border-top:1px solid darkGray;
                                            border-bottom:1px solid darkGray;
                                            border-right:1px solid darkGray;
                                            border-top-right-radius:10px;
                                            border-bottom-right-radius:10px;
                                          }
                                          QLabel#wenti_text_lable{
                                            border:none;
                                            font-size:16px;
                                            font-weight:700;
                                            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                                          }
                                        ''')
        self.right_widget_xiazai.setStyleSheet('''
                          QWidget#right_widget_xiazai{
                            color:#232C51;
                            background:white;
                            border-top:1px solid darkGray;
                            border-bottom:1px solid darkGray;
                            border-right:1px solid darkGray;
                            border-top-right-radius:10px;
                            border-bottom-right-radius:10px;
                          }
                        ''')

        self.right_bar_widget_appkey_input.setStyleSheet(
            '''QLineEdit{
                border:1px solid gray;
                width:75px;
                border-radius:10px;
                padding:2px 4px;
            }''')
        self.right_bar_widget_token_input.setStyleSheet(
            '''QLineEdit{
                border:1px solid gray;
                width:75px;
                border-radius:10px;
                padding:2px 4px;
            }''')
        self.right_bar_widget_speech_rate_input.setStyleSheet(
            '''QLineEdit{
                border:1px solid gray;
                width:75px;
                border-radius:10px;
                padding:2px 4px;
            }''')
        self.right_bar_widget_volume_input.setStyleSheet(
            '''QLineEdit{
                border:1px solid gray;
                width:75px;
                border-radius:10px;
                padding:2px 4px;
            }''')

        self.test_voice_button.setStyleSheet(
            '''QPushButton{
                    background:#1C86EE;border-radius:6px;
                    min-height: 25px; 
                    min-width: 100px;  
                    max-width: 100px; 
                    max-height: 25px;
            }QPushButton:hover{background:#436EEE;}''')
        self.xiazai_button.setStyleSheet(
            '''QPushButton{
                    background:#1C86EE;border-radius:6px;
                    min-height: 50px; 
                    min-width: 400px;  
                    max-width: 400px; 
                    max-height: 50px;
            }QPushButton:hover{background:#436EEE;}''')
        self.compose_voice_button.setStyleSheet(
            '''QPushButton{
                    background:#1C86EE;border-radius:6px;
                    min-height: 25px; 
                    min-width: 100px;  
                    max-width: 100px; 
                    max-height: 25px;
                    font-weight:bold;
            }QPushButton:hover{background:#436EEE;}''')
        self.right_bar_widget_text_input.setStyleSheet(
            '''QTextEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
            }''')
        self.right_bar_widget_format_input.setStyleSheet(
            '''QComboBox{
                border:1px solid gray;
                width:75px;
                border-radius:10px;
                padding:2px 4px;
            }''')
        self.right_bar_widget_voice_input.setStyleSheet(
            '''QComboBox{
                border:1px solid gray;
                width:75px;
                border-radius:10px;
                padding:2px 4px;
            }''')



        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.main_widget.setStyleSheet('''
            QWidget#left_widget{
            background:gray;
            border-top:1px solid white;
            border-bottom:1px solid white;
            border-left:1px solid white;
            border-top-left-radius:10px;
            border-bottom-left-radius:10px;
            }
            ''')

        self.main_layout.setSpacing(0)


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    logging.info('开始记录'.center(80, '*'))
    main()
    logging.info('结束记录'.center(80, '*'))