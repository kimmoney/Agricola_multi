import sys,traceback,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'py'))
# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images'))
# print(sys.path)
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt,QUrl
from PyQt5 import uic
from qcr_converter import *
from qcr_converter import run_pyrcc5
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
import sys,os,copy,random,socket,time,pickle
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent,QMediaPlaylist
from data.Algorithem.gameready import *
# from data.Algorithem.global_repository import *
import data.Algorithem.global_repository as status

def load_ui(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return uic.loadUiType(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ui'), relative_path+".ui"))[0]

def custom_exception_handler(exctype, value, tb):
    print(exctype,value,traceback.format_tb(tb))
    pass    

main_ui = load_ui("main")
setting_ui = load_ui("setting")
log_viewer_ui= load_ui("log_viewer")
greenroom_ui = load_ui("greenroom")
def trace(func):
    def wrapper(*args, **kwargs):
        # 출력 시 self 인수를 제거하여 가독성을 높임
        if args and isinstance(args[0], object):
            print(f"Calling {func.__name__} with args: {args[1:]} and kwargs: {kwargs}")
        else:
            print(f"Calling {func.__name__} with args: {args} and kwargs: {kwargs}")
        
        result = func(*args, **kwargs)
        
        print(f"{func.__name__} finished")
        return result
    
    return wrapper



import socket,time,pickle

