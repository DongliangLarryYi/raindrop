# RainDrop

一个极简白噪音App，只做一件事：播放下雨声，帮助用户入睡或专注。

## Why

这个项目是我从"学习技术"到"用技术交付产品"的跨越。面对AI浪潮，我选择主动实践而不是被动学习。一个能装在手机上的App，比任何课程证书都更能证明我的能力。

## 功能

- 播放/暂停下雨声（无缝循环）
- 定时关闭（15 / 30 / 60 分钟）

## 技术栈

- Python 3.12
- Flet（基于 Flutter 的 Python UI 框架）
- 打包：`flet build apk`

## 本地运行

```bash
cd ~/Documents/Projects/raindrop
python3.12 -m venv venv
source venv/bin/activate
pip install flet
python main.py
```
