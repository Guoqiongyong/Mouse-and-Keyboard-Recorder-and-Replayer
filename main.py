import time
import json
import os
from pynput import mouse, keyboard
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox  # 弹出框
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key, KeyCode

SPECIAL_KEYS = {
    'backspace': Key.backspace,
    'space': Key.space,
    'enter': Key.enter,
    'shift': Key.shift,
    'ctrl': Key.ctrl,
    'alt': Key.alt,
    'esc': Key.esc,
    'tab': Key.tab,
    'caps_lock': Key.caps_lock,
    'num_lock': Key.num_lock,
    'scroll_lock': Key.scroll_lock,
    'pause': Key.pause,
    'f1': Key.f1,
    'f2': Key.f2,
    'f3': Key.f3,
    'f4': Key.f4,
    'f5': Key.f5,
    'f6': Key.f6,
    'f7': Key.f7,
    'f8': Key.f8,
    'f9': Key.f9,
    'f10': Key.f10,
    'f11': Key.f11,
    'f12': Key.f12,
    'windows': Key.cmd,  # Windows键
}

class ActionRecorder:
    def __init__(self):
        self.actions = []  # 存储行为
        self.is_recording = False  # 是否正在录制
        self.listener = None  # 鼠标监听器
        self.keyboard_listener = None  # 键盘监听器
        self.start_time = None  # 用于计算相对时间
        self.filename = None  # 用于保存文件名

    def start_recording(self, filename):
        self.actions.clear()
        self.start_time = time.time()  # 记录开始时间
        self.is_recording = True
        self.filename = filename  # 保存文件名
        self.listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.listener.start()
        self.keyboard_listener.start()

    def stop_recording(self):
        self.listener.stop()
        self.keyboard_listener.stop()
        self.is_recording = False
        # 停止录制后自动保存
        if self.filename:
            self.save_actions(self.filename)

    def on_move(self, x, y):
        if self.is_recording:
            elapsed_time = time.time() - self.start_time
            self.actions.append({"type": "move", "time": elapsed_time, "x": x, "y": y})

    def on_click(self, x, y, button, pressed):
        if self.is_recording:
            elapsed_time = time.time() - self.start_time
            action_type = "click_down" if pressed else "click_up"
            self.actions.append({"type": action_type, "time": elapsed_time, "x": x, "y": y, "button": str(button)})

    def on_scroll(self, x, y, dx, dy):
        if self.is_recording:
            elapsed_time = time.time() - self.start_time
            self.actions.append({"type": "scroll", "time": elapsed_time, "x": x, "y": y, "dx": dx, "dy": dy})

    def on_key_press(self, key):
        if self.is_recording:
            elapsed_time = time.time() - self.start_time
            key_name = str(key).replace("'", "")  # 获取按键的名称
            self.actions.append({"type": "key_down", "time": elapsed_time, "key": key_name})

    def on_key_release(self, key):
        if self.is_recording:
            elapsed_time = time.time() - self.start_time
            key_name = str(key).replace("'", "")
            self.actions.append({"type": "key_up", "time": elapsed_time, "key": key_name})
            if key == Key.esc:  # 停止监听
                return False

    def save_actions(self, filename):
        try:
            with open(filename, 'w') as f:
                json.dump(self.actions, f)
            messagebox.showinfo("保存成功", "行为记录已成功保存！")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存行为记录时出错: {e}")

    def load_actions(self, filename):
        try:
            with open(filename, 'r') as f:
                self.actions = json.load(f)
            messagebox.showinfo("加载成功", "行为记录已成功加载！")
        except Exception as e:
            messagebox.showerror("加载失败", f"加载行为记录时出错: {e}")

    def replay_actions(self, repeat_count=1):
        # 使用固定的时间间隔
        step_time = 0.01  # 每次操作后等待的最小时间间隔，单位秒
        start_time = time.time()  # 获取当前时间
        for _ in range(repeat_count):
            for action in self.actions:
                # 计算操作的目标时间
                action_time = start_time + action["time"]
                time.sleep(max(0, action_time - time.time()))  # 保证不会出现负值的延迟
                
                # 执行鼠标或键盘操作
                self._perform_action(action)

    def _perform_action(self, action):
        mouse_controller = MouseController()
        keyboard_controller = KeyboardController()

        if action["type"] == "move":
            mouse_controller.position = (action["x"], action["y"])
            print(f"Moved mouse to: ({action['x']}, {action['y']})")

        elif action["type"] == "click_down" or action["type"] == "click_up":
            button = mouse.Button.left if "Button.left" in action["button"] else mouse.Button.right
            if action["type"] == "click_down":
                mouse_controller.press(button)
            else:
                mouse_controller.release(button)

        elif action["type"] == "scroll":
            mouse_controller.scroll(action["dx"], action["dy"])

        elif action["type"] == "key_down":
            key_name = action["key"]
            # 检查特殊键
            if key_name in SPECIAL_KEYS:
                keyboard_controller.press(SPECIAL_KEYS[key_name])  # 按下特殊键
            # 检查单个字符键
            elif len(key_name) == 1:
                keyboard_controller.press(KeyCode.from_char(key_name))  # 按下字符键
            else:
                print(f"Skipping unknown key press: {key_name}")

        elif action["type"] == "key_up":
            key_name = action["key"]
            # 检查特殊键
            if key_name in SPECIAL_KEYS:
                keyboard_controller.release(SPECIAL_KEYS[key_name])  # 释放特殊键
            # 检查单个字符键
            elif len(key_name) == 1:
                keyboard_controller.release(KeyCode.from_char(key_name))  # 释放字符键
            else:
                print(f"Skipping unknown key release: {key_name}")


# UI 部分
class ActionRecorderUI:
    def __init__(self, master):
        self.master = master
        self.master.title("行为录制器")
        self.master.geometry("500x300")

        self.recorder = ActionRecorder()

        self.record_button = tk.Button(self.master, text="开始录制", command=self.toggle_recording)
        self.record_button.pack(pady=20)

        self.save_button = tk.Button(self.master, text="保存录制", command=self.save_action, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        self.load_button = tk.Button(self.master, text="加载录制", command=self.load_action)
        self.load_button.pack(pady=10)

        self.replay_button = tk.Button(self.master, text="重放录制", command=self.replay_action)
        self.replay_button.pack(pady=10)

        self.quit_button = tk.Button(self.master, text="退出", command=self.master.quit)
        self.quit_button.pack(pady=20)

    def toggle_recording(self):
        if self.recorder.is_recording:
            self.recorder.stop_recording()  # 停止录制并自动保存
            self.record_button.config(text="开始录制")
            self.save_button.config(state=tk.NORMAL)
        else:
            filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if filename:
                self.recorder.start_recording(filename)
                self.record_button.config(text="停止录制")
                self.save_button.config(state=tk.DISABLED)

    def save_action(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            self.recorder.save_actions(filename)

    def load_action(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            self.recorder.load_actions(filename)

    def replay_action(self):
        if self.recorder.actions:
            self.recorder.replay_actions()


if __name__ == "__main__":
    root = tk.Tk()
    app = ActionRecorderUI(root)
    root.mainloop()
