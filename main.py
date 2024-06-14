from PyQt5.QtGui import QMouseEvent
from data.py.def_list import *
# sys.excepthook = custom_exception_handler
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
        self.setting = {"background_media":False,"event_media":True,"name":""}
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
        self.back_far. clicked.connect(lambda:self.change_main_page("menu"))
        self.back_greenroom. clicked.connect(lambda:self.change_main_page("menu"))
        
        self.log_popup = Log_viewer(self)
        
        self.init_music()
        self.Setting_dialog = Setting(self)
        #####init
        self.main_Stacked_Widget.setCurrentIndex(0)
    
    def resizeEvent(self, event):self.resize(event.size().width(), int(event.size().width() / (16 / 9)))

    def func_sign_up(self):
        name = self.input_sign_up_name.text()
        if name:
            self.setting["name"] = name
            self.change_main_page("menu")
            print(self.setting)
            self.client = Nomal_Client(name)
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
        glist =self.client.get_list_Green_room()
        print(glist)
        for greenroom in glist:
            gr = Greenroom_Class(self)
            gr.ping.setText(greenroom[1].split("|")[2])
            gr.host.setText(greenroom[1].split("|")[1])
            gr.ip.setText(greenroom[0])
            gr.count.setText(f"{greenroom[1].split("|")[1]}/4")
            self.greenroom_near_layout.addWidget(gr)




    def clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()





class Greenroom_Class(QWidget, greenroom_ui) :
    @trace
    def __init__(self,main) :
        
        super().__init__()
        self.setupUi(self)
        self.main = main


    # def mousePressEvent(self,event) :
    #     self.main.client.server_ip = self.ip.text()
    #     self.main.client.send_client("JOIN")
    #     main.change_main_page("greenroom")
    #     print(game_status_repository.now_turn_player)
        
    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        self.main.client.server_ip = self.ip.text()
        self.main.client.send_client("JOIN")
        main.change_main_page("greenroom")
        return super().mousePressEvent(a0)
        







        
class Nomal_Client():
    def __init__(self,name):
        self.name = "|"+name
        self.player_num = 0
        self.ip_list = []
        self.server_ip = "192.168.0.5"
        
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
                print((ip,response))
                s.close()
                self.ip_list.append((ip,response))
                print(f"connecting ip : {ip}")
            except:pass
            # except (socket.timeout, socket.error):
            #     pass
        return self.ip_list
    
    def send_client(self,message, server_port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, server_port))
        message +=self.name
        t = time.time()
        self.client_socket.send(message.encode())
        response = self.client_socket.recv(9192)
        self.client_socket.close()
        try:
            response = response.decode()
            print(f"ping :{time.time() - t}ms")
            print(f'Received from server: {response}')
            if "player_num" in response:
                self.player_num == int(response.split('|')[1])
        except:
            global game_status_repository,round_status_repository,player_status_repository
            response = pickle.loads(response)
            game_status_repository = response[0]
            round_status_repository = response[1]
            player_status_repository = response[2]
            return game_status_repository,round_status_repository,player_status_repository
            # if game_status_repository.now_turn_player != self.player_num:
            #     self.send_client("wait")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Client_Class()
    global pprint
    pprint = main.pprint
    main.show()
    sys.exit(app.exec_())