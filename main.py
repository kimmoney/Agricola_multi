from PyQt5.QtCore import QObject
from PyQt5.QtGui import QMouseEvent
from data.py.def_list import *
sys.excepthook = custom_exception_handler
from data.py.images_rc import * 
from data.py.def_qt import *
# run_pyrcc5()


class Client_Class(QMainWindow, main_ui) :
    @trace
    def __init__(self) :
        global game_status_repository,round_status_repository,player_status_repository
            
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Fixed Aspect Ratio Window")
        # 메인스텍트위젯 
        self.setting = {"background_media":False,"event_media":True}
        self.name = ""
        self.change_main_page = lambda after_page: change_stacked_page(self,self.main_Stacked_Widget, after_page)
        self.timer_close,self.timer_open = QTimer(self),QTimer(self)

        self.btn_start.clicked.connect(lambda:self.change_main_page("sign_up"))

        self.btn_sign_up_confirm.clicked.connect(self.func_sign_up)
        self.btn_sign_up_exit.clicked.connect(lambda:self.change_main_page("start_page"))

        self.btn_main_greenroom_near.clicked.connect(lambda:self.change_main_page("greenroom_near"))
        self.btn_main_greenroom_near.clicked.connect(self.func_greenroom_near_show)
        self.btn_main_greenroom_far.clicked.connect(lambda:self.change_main_page("greenroom_far"))
        self.btn_main_setting.clicked.connect(self.open_setting)

        self.back_near.clicked.connect(lambda:self.change_main_page("menu"))
        self.near_ready.clicked.connect(self.func_near_ready)
        self.back_far. clicked.connect(lambda:self.change_main_page("menu"))
        self.pushButton_2. clicked.connect(lambda:self.change_main_page("menu"))
        self.pushButton.clicked.connect(self.test)
        self.pushButton_3.clicked.connect(self.next_turn)
        self.pushButton_4.clicked.connect(self.push_data)

        # self.back_greenroom. clicked.connect(lambda:self.change_main_page("menu"))
        # self.back_greenroom. clicked.connect(lambda:print(game_status_repository.status))
        # self.back_greenroom. clicked.connect(self.update_status_all)
        self.back_greenroom. clicked.connect(lambda:self.change_main_page("menu"))
        self.menu.showEvent = lambda event: main_showEvent(self, event)
        self.greenroom.showEvent = lambda event: greenroom_showEvent(self, event)
        self.log_popup = Log_viewer(self)
        
        self.init_music()
        self.Setting_dialog = Setting(self)
        #####init
        self.main_Stacked_Widget.setCurrentIndex(0)
        self.client = nomal_client_Thread(self)
        self.client.progress.connect(self.update_status_all)
        self.btn_main_greenroom_near.clicked.connect(self.client.start)
        
    def resizeEvent(self, event):self.resize(event.size().width(), int(event.size().width() / (16 / 9)))
    def test(self):
        exec(self.lineEdit.text())
        self.push_data()
    def func_sign_up(self):
        name = self.input_sign_up_name.text()
        print(name)
        if name:
            self.name = name
            self.client.name = name
            self.change_main_page("menu")
            print(self.setting)
            
        else:
            pprint("닉네임을 입력해주세요.")

    @trace
    def init_music(self):
        #음악 재생
        self.mediaPlayer,self.mediaPlaylist = QMediaPlayer(),QMediaPlaylist()
        self.mediaPlaylist.clear()
        self.mediaPlaylist.addMedia(QMediaContent(QUrl.fromLocalFile(r'data\media\backround.mp3')))
        self.mediaPlaylist.setPlaybackMode(QMediaPlaylist.Loop)
        self.mediaPlayer.setPlaylist(self.mediaPlaylist)
        self.mediaPlayer.play()
        self.set_music()
    @trace
    def set_music(self):
        match self.setting["background_media"]:
            case True:
                self.mediaPlayer.setMuted(False)
            case False:
                self.mediaPlayer.setMuted(True)

    def open_setting(self):
        self.Setting_dialog.exec_()

    def pprint(self,text):
        self.log_popup.logging(text)
        print(text)

    def func_greenroom_near_show(self):
        self.clearLayout(self.greenroom_near_layout)
        self.client.message = "get_list_Green_room"

        
    def func_greenroom_near_thread_finished(self):
        for greenroom in self.glist:
            gr = Greenroom_Class(self)
            print(greenroom)
            gr.ping.setText(str(greenroom[2]))
            gr.host.setText(greenroom[1][1])
            gr.ip.setText(greenroom[0])
            gr.count.setText(f"{greenroom[1][2]}/4")
            self.greenroom_near_layout.addWidget(gr)



    def clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
    @trace
    def update_status_all(self):
        print("update")
        print(game_status_repository.now_turn_player)
        self.func_greenroom_near_thread_finished()
        print(game_status_repository.status)
        if game_status_repository.status == "start" and self.main_Stacked_Widget.currentWidget() != self.start_page:
            self.change_main_page("game")
        if game_status_repository.status == "start":
            self.data_test_11.setText(str(game_status_repository.__dict__))
            self.data_test_12.setText(str(player_status_repository[self.name].__dict__))
            self.data_test_13.setText(str(player_status_repository[self.name].card.__dict__))
            self.data_test_0.setText(str(game_status_repository.now_turn_player == self.name))
            self.pushButton_3.setEnabled(self.name == game_status_repository.now_turn_player)
            self.pushButton_4.setEnabled(self.name == game_status_repository.now_turn_player)
        # self.data_test_12.setText(str(player_status_repository[player_num]))
        # self.data_test_.setText(str())
        # self.data_test_.setText(str())
        # self.data_test_.setText(str())
        # self.data_test_.setText(str())
        # self.data_test_.setText(str())
        # elif game_status_repository.status == "ready":
            # main.change_main_page("greenroom")

    def push_data(self):
        game_status_repository.next = True
        self.client.message = "process"
        self.update_status_all()
    def next_turn(self):
        game_status_repository.next_player()
        self.push_data()

    def func_near_ready(self):
        self.near_ready.setEnabled(False)
        player_status_repository[self.name].ready = True
        self.client.message="process"
    













def main_showEvent(self,event):
    game_status_repository.status="ready"
    self.client.quit()
def greenroom_showEvent(self,event):
    self.near_ready.setEnabled(True)
class Greenroom_Class(QWidget, greenroom_ui) :
    @trace
    def __init__(self,main) :
        
        super().__init__()
        self.setupUi(self)
        self.main = main
        
    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        self.main.client.server_ip = self.ip.text()
        
        # self.main.change_main_page("greenroom")
        self.main.main_Stacked_Widget.setCurrentWidget(self.main.greenroom)
        self.main.update()
        self.main.client.message = "JOIN"
        return super().mousePressEvent(a0)
        





class nomal_client_Thread(QThread):
    # 작업이 완료되었음을 알리는 시그널
    # finished = pyqtSignal()
    progress = pyqtSignal()
    def __init__(self, parent) :
        super().__init__()
        self.parent = parent
        self.name = parent.name
        self.message = ""
    def run(self):
        print("이름은",self.name)
        print(self.name)
        self.Client_cs = Nomal_Client(self.name)
        self.Client_cs.progress.connect(self.progress.emit)
        while True:
            if self.message == "get_list_Green_room":
                self.parent.glist = self.get_list_Green_room()
                self.progress.emit()

                # self.parent.func_greenroom_near_thread_finished()
            elif self.message!="":
                global game_status_repository,round_status_repository,player_status_repository
                self.Client_cs.send_client(self.message)
                print(game_status_repository.status)
                self.progress.emit()
            self.message = ""
    def get_list_Green_room(self):
        return self.Client_cs.get_list_Green_room()
        # self.finished.emit()


import socket,time,pickle
class Nomal_Client(QObject):
    progress = pyqtSignal()
    def __init__(self,name):
        super().__init__()
        self.name = name
        self.ip_list = []
        self.server_ip = "192.168.0.5"
        
    def get_list_Green_room(self):
        global game_status_repository,round_status_repository,player_status_repository
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
                s.send(pickle.dumps(["ping",self.name]))
                response = pickle.loads(s.recv(1024))
                print((ip,response))
                s.close()
                self.ip_list.append((ip,response,t-time.time()))
                print(f"connecting ip : {ip}")
            except:pass
            # except (socket.timeout, socket.error):
            #     pass
        return self.ip_list
    
    def send_client(self,message, server_port=12345):
        global game_status_repository,round_status_repository,player_status_repository
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, server_port))
        if message == "process":
            message =[game_status_repository,round_status_repository,player_status_repository,"",""]
        else:
            message = [message]
        message.append(self.name)
        message.append(self.name)
        t = time.time()
        self.client_socket.send(pickle.dumps(message))
        response = self.client_socket.recv(9192)
        print(len(response))
        self.client_socket.close()
        response = pickle.loads(response)
        print(response)

        if len(response) < 4:
            print(f"ping :{time.time() - t}ms")
            print(f'Received from server: {response}')
            #입장 완료
        else:
            game_status_repository = response[0]
            round_status_repository = response[1]
            player_status_repository = response[2]
            print(player_status_repository)
            print(game_status_repository.now_turn_player, self.name)
            self.progress.emit()
            if game_status_repository.now_turn_player != self.name and game_status_repository.status == "start":
                self.send_client("process")

            if game_status_repository.status == "greenroom" and player_status_repository[self.name].ready:
                self.send_client("process")
 




if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Client_Class()
    global pprint
    pprint = main.pprint
    main.show()
    sys.exit(app.exec_())