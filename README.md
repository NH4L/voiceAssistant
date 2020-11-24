@[TOC]([配音助手] 更新（1.3） 阿里云小姐姐配音软件)

>推荐系统：windows10/7
>推荐系统类型：64位操作系统
>推荐使用人群：视频制作者，配音制作者

使用前请先查看软件（**配音助手1.0**）介绍：
csdn: [https://blog.csdn.net/LeeGe666/article/details/106604378](https://blog.csdn.net/LeeGe666/article/details/106604378)
知乎：[https://zhuanlan.zhihu.com/p/146489438](https://zhuanlan.zhihu.com/p/146489438)

**配音助手下载地址**：
[蓝奏云 配音助手1.3.zip](https://nh4l.lanzous.com/iZVDSg5kccf)
[微云   配音助手1.3.zip](https://share.weiyun.com/kddB9ikC)
[自建服务器 配音助手1.3.zip](https://www.aysst.cn/files/%E9%85%8D%E9%9F%B3%E5%8A%A9%E6%89%8B1.3.zip)

>**声明**
>本软件只适用于配音者，视频制作者
>不适用于超大规模（10万字以上）超长文本配音
>本软件完全开源并免费，商用产生费用为阿里云根据合成字数及时长产生，和本软件无关
>

## 更新内容（1.3）[windows 10 2004版本及以下]
#### 1、增加商用音色功能（每次合成<10万字，10分钟内生成）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200828205558298.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xlZUdlNjY2,size_16,color_FFFFFF,t_70#pic_center)
所加音色为**长文本语音合成商用**！非商用音色免费！
具体价格细节可查看阿里云
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200828205812909.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xlZUdlNjY2,size_16,color_FFFFFF,t_70#pic_center)

下面介绍如果开通商用：
进入**智能语音交互控制台**
选择长文本语音合成（文学类为商用，音色只能应用于长文本）
点击**服务开通与购买**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200828210147641.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xlZUdlNjY2,size_16,color_FFFFFF,t_70#pic_center)
全部选择商用开通即可，**不使用不会产生费用**！
**不建议购买时长包，生成过程中产生多少费用支付即可！大规模使用者可能会产生较多费用，普通用户不建议开通（使用不慎可产生大量费用）**！
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200828210343321.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xlZUdlNjY2,size_16,color_FFFFFF,t_70#pic_center)


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

**感谢**：@南宫涵， @梦想拉长了身影，等网友的反馈与建议

**github**开源: [https://github.com/NH4L/voiceAssistant ](https://github.com/NH4L/voiceAssistant)

