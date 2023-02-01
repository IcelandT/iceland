# -*- coding: utf-8 -*-
import os


def run(*args):
    """ 收集设备上设定的所有环境变量 """
    print("[*] 当前在 environment 模块中.")
    return os.environ