# -*- coding: utf-8 -*-
import os


def run(*args):
    """ 返回路径下的所有文件名 """
    print("[*] 当前在 dirlister 模块中.")
    files = os.listdir(".")
    return str(files)
