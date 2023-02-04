# -*- coding: utf-8 -*-
""" 截取屏幕 """
import win32api
import base64
import win32com
import win32con
import win32gui
import win32ui


def get_dimensions():
    """ 获取屏幕尺寸 """
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    print("屏幕大小:", width, height, left, top)
    return width, height, left, top


def screenshot(name="screenshot"):
    """ 截取屏幕 """
    # 获取整个桌面的句柄
    hdesktop = win32gui.GetDesktopWindow()
    width, height, left, top = get_dimensions()

    # 调用GetWindowDC创建一个设备上下文
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    # CreateCompatibleDC() 创建基于内存的设备上下文
    mem_dc = img_dc.CreateCompatibleDC()
    # CreateBitmap() 创建位图对象 将格式设置成和左面设备上下文相符
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    # 将内存设备上下文指向要捕获的位图对象
    mem_dc.SelectObject(screenshot)
    # BitBlt() 将桌面图片逐位复制并保存到内存上下文中
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
    # SaveBitmapFile() 保存到磁盘上
    screenshot.SaveBitmapFile(mem_dc, f"{name}.bmp")

    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())


def run():
    screenshot()
    with open("screenshotter.bmp") as f:
        img = f.read()
    return img


if __name__ == '__main__':
    screenshot()