@[TOC]([配音助手] 更新（1.2） 阿里云小姐姐配音软件)

>推荐系统：windows10/7
>推荐系统类型：64位操作系统
>推荐使用人群：视频制作者，配音制作者

使用前请先查看软件（配音助手1.0）介绍：
csdn: [https://blog.csdn.net/LeeGe666/article/details/106604378](https://blog.csdn.net/LeeGe666/article/details/106604378)
知乎：[https://zhuanlan.zhihu.com/p/146489438](https://zhuanlan.zhihu.com/p/146489438)

下载地址：[https://www.aysst.cn/files/配音助手1.2.zip](https://www.aysst.cn/files/%E9%85%8D%E9%9F%B3%E5%8A%A9%E6%89%8B1.2.zip)
## 更新内容（1.2）[windows 10 2004版本及以下]
#### 1、解决window10 2004版本卡死问题
原因：2004版本将底层适配包更新，所以qt官方也将底层更新，包重新适配。由于我是上一代版本qt，对2004不兼容，造成前遇到弹窗卡死的情况。

解决：更新开发包，发现新的开发环境下不能使用原有代码，因为子线程不能独立拥有弹窗，于是利用Signal将信号传递到主线程中使用，不发生卡死现象。


## 更新内容（1.1）[windows 10 1909版本及以下]

#### 1、增加图标
左上角增加**最小化**，**最大化**，**关闭** 图标，更加直观。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200612155609994.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xlZUdlNjY2,size_16,color_FFFFFF,t_70)
#### 2、取消用户自定义输入文件名
如上图，取消**文件名输入框**，采用**日期自动生成**，主要是为了避免用户语音合成时讲上一个同名称文件覆盖。
下载文件如下：**年月日_时分秒** ， _0, _1, _2为同一次语音合成生成的三个文件。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200612160021787.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xlZUdlNjY2,size_16,color_FFFFFF,t_70)
#### 3、多线程合成音频提高速度
多线程合成音频，**并发数**为2，速度较上个版本提高一倍左右，由于阿里云的**免费项目限制**，**最高并发数为2**，由于用户基本不是大量语音合成需求者，且此并发数以后版本不做改变，因为一般用户为视频配音者，若有需求大量文本（>10000字）音频合成需求（需收费），请私聊我。

#### 4、保存上次语音合成记录
在进行第一次语音合成后，会在本目录下生成 **voice_data.json**文件，其中保存语音合成信息：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200612161129553.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xlZUdlNjY2,size_16,color_FFFFFF,t_70)
下次打开软件时，会自动读取json中数据到输入框中，避免用户多次繁琐输入appkey，token，但文本任需自己输入。
如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200612161310237.png)
#### 5、细节修改
使用说明中，网址可以直接链接到浏览器，方便用户查看使用说明。
文本可选择。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200612161407476.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xlZUdlNjY2,size_16,color_FFFFFF,t_70)
#### 6、修复点击音频合成会一直卡住的bug
原因为日志生成代码出错，导致音频文件已经合成，但得不到提示，需重启才可以重新运行。


## 一、软件介绍
意外发现阿里云语音合成效果非常不错，且某些音色非常真实好听，应网友要求，特意为没有代码方面经验的朋友制作了这款软件，方便大家更好的进行配音以及其他使用。


本软件基于pyqyt5绘制GUI，基于爬虫获取阿里云语音合成API，由于阿里云官方免费版有300字数限制，本软件利用标点符号（句号。）和限制字数构造了一种文本句子切割算法，将切割下来的字符分别进行语音合成，突破阿里云语音合成字数限制。
使用本软件前先查看博客
csdn：[https://blog.csdn.net/LeeGe666/article/details/105353599](https://blog.csdn.net/LeeGe666/article/details/105353599)
知乎：[https://zhuanlan.zhihu.com/p/123930042](https://zhuanlan.zhihu.com/p/123930042)

根据博客中教程，注册阿里云账户，创建智能语音交互项目，获取appkey和token。

## 二、软件使用
下载**配音助手.zip**，解压(解压路劲随意)后打开**配音助手.exe**,切勿删除该目录下的图片，图片为桌面显示图标，删除后软件不弄运行。

#### 2.1 语音合成页
采用半透明设计，左上角三个点依次为**最小化**，**最大化**，**关闭**，
输入框中的参数从第一步得到并填入，最后根据自身需求更改参数后即可进行语音合成。
音色选择可以点击配音试听，跳转到阿里云官网中试听，选择自己需要的配音音色，即可进行音频合成。
下载好的文件在当前目录的**audioFiles目录**下
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200607170425534.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xlZUdlNjY2,size_16,color_FFFFFF,t_70)


#### 2.2 使用说明
点击第二个使用说明即可到达该页
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200607171522900.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xlZUdlNjY2,size_16,color_FFFFFF,t_70)
#### 2.3 下载管理

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200607171731670.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xlZUdlNjY2,size_16,color_FFFFFF,t_70)
点击打开后，即打开下载文件所在目录

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200607171835411.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xlZUdlNjY2,size_16,color_FFFFFF,t_70)
#### 2.4 反馈建议

![在这里插入图片描述](https://img-blog.csdnimg.cn/2020060717191840.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xlZUdlNjY2,size_16,color_FFFFFF,t_70)
#### 2.5 关于我们
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200607171954410.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xlZUdlNjY2,size_16,color_FFFFFF,t_70)
#### 2.6 遇到问题
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200607172026498.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xlZUdlNjY2,size_16,color_FFFFFF,t_70)
## 三、总结
由于时间原因，没有开发该软件对应的网站，本软件为免费软件，不收取任何费用，若遇到bug可以私信或者发送bug到邮箱中。
本软件也不会获取用户信息，只有下载音频的时候才会用到网络，请放心使用，若使用中有任何建议，请私信或邮箱。



**感谢**：@南宫涵， @梦想拉长了身影，等网友的反馈与建议

**github**开源: [https://github.com/NH4L/voiceAssistant ](https://github.com/NH4L/voiceAssistant)


