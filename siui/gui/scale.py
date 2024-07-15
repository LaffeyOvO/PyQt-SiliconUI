import ctypes
import os


def get_windows_scaling_factor():
    try:
        # 调用 Windows API 函数获取缩放比例
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        scaling_factor = user32.GetDpiForSystem()

        # 计算缩放比例
        print("缩放比例", scaling_factor / 96.0)
        return scaling_factor / 96.0

    except Exception as e:
        print("无法获取缩放比例，设置为1，错误:", e)
        return 1


def reload_scale_factor():
    os.environ['QT_SCALE_FACTOR'] = str(get_windows_scaling_factor())


def set_scale_factor(factor):
    os.environ['QT_SCALE_FACTOR'] = str(factor)