# 鼠标键盘行为记录与重现器

这是一个基于 **Python** 和 **Tkinter** 开发的桌面应用程序，用于录制鼠标和键盘的行为，并能够重现这些行为。

## 功能概述

- **录制**：记录鼠标移动、点击、滚动以及键盘按键操作。
- **保存**：将录制的行为保存为 `.json` 文件，方便以后重放。
- **加载**：可以加载以前保存的 `.json` 行为文件。
- **重放**：根据录制的行为，自动重现鼠标和键盘操作。

## 环境要求

为了运行此应用程序，你需要在你的计算机上安装以下库：pynput tkinter

### 安装指引

#推荐虚拟环境运行
```bash
# 克隆储存库
git clone https://github.com/Guoqiongyong/Mouse-and-Keyboard-Recorder-and-Replayer.git
```bash
# 打开目录
cd Mouse-and-Keyboard-Recorder-and-Replayer
```bash
# 创建名为 myenv 的虚拟环境
python -m venv myenv
```bash
# 激活虚拟环境。在终端或命令提示符中运行以下命令：
# 对于 Windows：
myenv\Scripts\activate
# 对于 macOS/Linux：
source myenv/bin/activate
# 安装依赖

```bash
pip install -r requirements.txt
# 运行脚本
python main.py

**Linux 安装(依赖文件单独安装)**

```bash
pip3 install pynput tkinter

***Windows 安装(依赖文件单独安装)***

```bash
pip install pynput tkinter




