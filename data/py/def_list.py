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

import sys,os,copy,random,socket,time,pickle
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent,QMediaPlaylist
from data.Algorithem.global_repository import *


def load_ui(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return uic.loadUiType(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ui'), relative_path+".ui"))[0]

def custom_exception_handler(exctype, value, tb):
    print(exctype,value,traceback.format_tb(tb))
    pass    

main_ui = load_ui("main")
setting_ui = load_ui("setting")
log_viewer_ui= load_ui("log_viewer")

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




class Nomal_Client():
    def __init__(self,name):
        self.name = "|"+name
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.ip_list = []
        
    def get_list_Green_room(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        myadress = ip_address
        self.ip_list = []
        for i in range(255):
            ip =  ".".join(myadress.split(".")[:-1])+f".{i}"
            # try:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.01)  # 타임아웃을 0.01초로 설정
                s.connect((ip, 12345))
                t = time.time()
                s.send(f"ping|{self.name}".encode())
                response = s.recv(1024).decode()
                print(f"ping :{time.time() - t}ms")
                s.close()
                self.ip_list.append(ip)
                print(f"connecting ip : {ip}")
            except:pass
            # except (socket.timeout, socket.error):
            #     pass
        return self.ip_list
    
    def send_client(self,message,server_ip="192.168.0.5", server_port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, server_port))
        message +=self.name
        t = time.time()
        self.client_socket.send(message.encode())
        response = self.client_socket.recv(9192)
        self.client_socket.close()
        try:
            response = response.decode()
            print(f"ping :{time.time() - t}ms")
            print(f'Received from server: {response}')
        except:
            response = pickle.loads(response)
        return response


# if __name__ == "__main__":
#     sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#     from main import *
#     Start_Client()

