# Keqi tts server integration for Home Assistant

本项目是keqi tts集成到Home Assistant的代码库，相关链接https://github.com/xiaokebulan/keqi_tts.git


## 安装

下载并复制`custom_components/ke_qi_tts`文件夹到HomeAssistant根目录下的`custom_components`文件夹

```
tts:
  - platform: ke_qi_tts
    language: zh
    url: http://www.keqi.server:5000/tts （www.keqi.server替换成KEQI TTS SERVERD的ip）
```

## 使用范例

```
service: tts.ke_qi_tts_say
data:
  entity_id: media_player.keqiketing
  message: 今天天气真好啊
```

## 欢迎加入知识星球或者QQ群讨论，知识星球里面提供项目的模型文件、相关资料以及国内的加速镜像文件。

qq群811427872

<img src="static/xing.jpg" width="300">


## 打赏作者

<img src="static/coffee.jpg" width="300">
  您的支持是我继续开源的动力！

