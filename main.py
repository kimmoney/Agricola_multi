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
            
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Fixed Aspect Ratio Window")
        # 메인스텍트위젯 
        self.setting = {"background_media":False,"event_media":True}
        self.name = ""
        self.input_sign_up_name.setText(f"김도훈{time.time_ns()}")
        self.client = nomal_client_Thread(self,self.name)
        self.Server_Client = Server_client_Thread(self)
        self.change_main_page = lambda after_page: change_stacked_page(self,self.main_Stacked_Widget, after_page)
        self.timer_close,self.timer_open = QTimer(self),QTimer(self)

        self.btn_start.clicked.connect(lambda:self.change_main_page("sign_up"))

        self.btn_sign_up_confirm.clicked.connect(self.func_sign_up)
        self.btn_sign_up_exit.clicked.connect(lambda:self.change_main_page("start_page"))

        self.btn_main_greenroom_near.   clicked.connect(lambda:self.change_main_page("greenroom_near"))
        
        self.btn_main_greenroom_far.    clicked.connect(lambda:self.change_main_page("greenroom_far"))



        self.btn_main_setting.clicked.connect(self.open_setting)

        self.near_back.     clicked.connect(self.client.exit)
        self.near_back.     clicked.connect(lambda:self.change_main_page("menu"))
        self.near_ready.    clicked.connect(self.func_near_ready)
        self.far_back.      clicked.connect(lambda:self.change_main_page("menu"))
        self.pushButton_2.  clicked.connect(lambda:self.client.message_input("exit"))
        self.pushButton_2.  clicked.connect(lambda:self.change_main_page("menu"))

        self.near_new.clicked.connect(self.Server_Client.start)


        self.pushButton.clicked.connect(self.test)
        self.pushButton_4.clicked.connect(self.push_data)
        self.pushButton_3.clicked.connect(self.next_turn)
        self.back_greenroom. clicked.connect(lambda:self.change_main_page("menu"))
        self.menu.showEvent = lambda event: self.main_showEvent(event)
        self.greenroom.showEvent = lambda event: greenroom_showEvent(self, event)
        self.log_popup = Log_viewer(self)
        
        self.init_music()
        self.Setting_dialog = Setting(self)
        #####init
        self.main_Stacked_Widget.setCurrentIndex(0)
        print(type(self))
        self.client.progress.connect(self.update_status_all)
        self.client.add_greenroom.connect(lambda list : self.add_greenroom(list))
        # self.btn_main_greenroom_near.clicked.connect(lambda name=self.name:self.client.__init__(name))
        self.btn_main_greenroom_near.clicked.connect(self.make_client)
        # self.btn_main_greenroom_near.   clicked.connect(self.func_greenroom_near_show)
    def make_client(self):
        self.clearLayout(self.greenroom_near_layout)
        self.client.message = "get_list_Green_room"
        self.client.start()

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
            self.Server_Client.name = name
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

    def add_greenroom(self,greenroom):
        print("add_greenroom")
        self.greenroom_dict = {}
        gr = Greenroom_Class(self)
        print(greenroom)
        gr.ping.setText(str(greenroom[2]))
        gr.host.setText(greenroom[1][1])
        gr.ip.setText(greenroom[0])
        gr.count.setText(f"{greenroom[1][2]}/4")
        self.greenroom_dict[greenroom[0]] = gr
        self.clearLayout(self.greenroom_near_layout)
        for gr in self.greenroom_dict.values():
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
        print(status.game_status_repository.now_turn_player)
        # self.func_greenroom_near_thread_finished()
        print(status.game_status_repository.status)
        for i in range(4):
            try:
                name = status.game_status_repository.players[i]        
                getattr(self,f"greenroom_player_name_{i}").setText(name)
            except:
                getattr(self,f"greenroom_player_name_{i}").setText(f"플레이어 {i+1}")
        if status.game_status_repository.status == "start" and self.main_Stacked_Widget.currentWidget() != self.start_page:
            self.change_main_page("game")
        if status.game_status_repository.status == "start":
            self.data_test_11.setText(str(status.game_status_repository.__dict__))
            self.data_test_12.setText(str(status.player_status_repository[self.name].__dict__))
            self.data_test_13.setText(str(status.player_status_repository[self.name].card.__dict__))
            self.data_test_0.setText(str(status.game_status_repository.now_turn_player == self.name))
            self.pushButton_3.setEnabled(self.name == status.game_status_repository.now_turn_player)
            self.pushButton_4.setEnabled(self.name == status.game_status_repository.now_turn_player)

        

    def push_data(self):
        status.game_status_repository.next = True
        self.client.message_input("process")
        self.update_status_all()

    def next_turn(self):
        status.game_status_repository.next_player()
        self.push_data()

    def func_near_ready(self):
        self.near_ready.setEnabled(False)
        status.player_status_repository.get(self.name,)
        status.player_status_repository[self.name].ready = True
        self.client.message="process"
    










    def main_showEvent(self,event):
        self.client.message_input("exit")
        status.game_status_repository.status="ready"
        self.client.quit()
        self.client.Client_cs.client_socket.close()
        self.Server_Client.Client_cs.server_socket.close()
        self.Server_Client.quit()
        print("메인화면")
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
    add_greenroom = pyqtSignal(list)
    def __init__(self, main,name) :
        super().__init__()
        self.parent = main
        self.name = name
        self.message = ""
        self.Client_cs = Nomal_Client(self.name)
    def run(self):
        print("이름은",self.name)
        print(self.name)
        self.Client_cs = Nomal_Client(self.name)
        self.Client_cs.progress.connect(self.progress.emit)
        self.Client_cs.add_greenroom.connect(self.add_greenroom.emit)
        while True:
            if self.message == "get_list_Green_room":
                self.Client_cs.get_list_Green_room()

                # self.parent.func_greenroom_near_thread_finished()
            elif self.message!="":
                self.Client_cs.send_client(self.message)
                # print(status.game_status_repository.status)
                self.progress.emit()
                self.message = ""
    def message_input(self,message):
        self.message = message
    def exit(self):
        self.message = "exit"




import socket,time,pickle
class Nomal_Client(QObject):
    progress = pyqtSignal()
    add_greenroom = pyqtSignal(list)
    def __init__(self,name):
        super().__init__()
        self.name = name
        self.ip_list = []
        self.server_ip = "192.168.0.5"
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def get_list_Green_room(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        # ip_address = s.getsockname()[0]
        ip_address = "192.168.0.1"
        s.close()
        myadress = ip_address
        self.ip_list = []
        for i in range(65):
            ip =  ".".join(myadress.split(".")[:-1])+f".{i}"
            # try:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.2)  # 타임아웃을 0.01초로 설정
                s.connect((ip, 12345))
                t = time.time()
                s.send(pickle.dumps(["ping",self.name]))
                response = pickle.loads(s.recv(1024))
                print((ip,response))
                s.close()

                self.add_greenroom.emit([ip,response,time.time()-t])
                print(f"connecting ip : {ip}")
            except:
                # print((ip,"fail"))
                pass
            # except (socket.timeout, socket.error):
            #     pass
        return self.ip_list
    
    def send_client(self,message, server_port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, server_port))
        if message == "process":
            message =[status.game_status_repository,status.round_status_repository,status.player_status_repository,"",""]
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
        # print("response : ",response)

        if len(response) < 4:
            if response == "exit":
                print("나가요~")
            print(f"ping :{time.time() - t}ms")
            print(f'Received from server: {response}')
            #입장 완료
        else:
            status.game_status_repository = response[0]
            status.round_status_repository = response[1]
            status.player_status_repository = response[2]
            self.progress.emit()
            if status.game_status_repository.now_turn_player != self.name and status.game_status_repository.status == "start":
                self.send_client("process")

            if status.game_status_repository.status == "greenroom" and status.player_status_repository[self.name].ready:
                self.send_client("process")
 









class Server_client_Thread(QThread):
    # 작업이 완료되었음을 알리는 시그널
    # finished = pyqtSignal()
    progress = pyqtSignal()
    def __init__(self, parent) :
        super().__init__()
        self.parent = parent
        self.name = parent.name
        self.message = ""
        self.Client_cs = Server_Client(self.name)
    def init(self):
        print("초기화 되었습니다")
        status.server_game_status.__init__()
        status.server_player_status = {}
    def run(self):
        print("서버가 열렸습니다.")
        self.init()
        print(self.name)
        self.Client_cs.start_recived()
class Server_Client():
    def __init__(self,name="HOST"):
        #포트 조회
        self.name = name
        # self.server_socket = self.start_server()
        self.player = {}
        # self.start_recieved()
        self.maximum_count = 4
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pass

    def start_server(self,host='0.0.0.0', port=12345):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f'Server listening on {host}:{port}') 
        self.status = "greenroom"
        return server_socket

    def start_recived(self):
        status.server_game_status.status = "greenroom"
        self.server_socket = self.start_server()
        while True:
            
            client_socket, addr = self.server_socket.accept()
            client_ip = addr[0]
            print(f'Connection from {client_ip}')
            data_ori = pickle.loads(client_socket.recv(9192))
            print("server : 데이터가 들어왔습니다.")
            # print(data_ori)


            if len(data_ori)<5:
                player = data_ori[1]
                data = data_ori[0]
                print(f"server : {player} - {data}.")

                match data:
                    case "ping":
                        print(f"server : {player} - {data}.")
                        print(['pong',self.name,len(self.player)])
                        client_socket.send(pickle.dumps(['pong',main.name,len(self.player)]))
                    case "OPEN?":
                        client_socket.send(pickle.dumps(['yes',]))
                    case "JOIN":
                        if len(self.player) ==self.maximum_count and (client_ip,player) not in self.player :
                            client_socket.send(pickle.dumps(['Full',]))
                        else:
                            print(f"{player} 플레이어가 입장했습니다. ")
                            status.add_player(player,client_ip)
                            status.server_game_status.num_players+=1
                            self.player[client_ip,player]=client_socket
                            client_socket.send(pickle.dumps([status.server_game_status,status.server_round_status,status.server_player_status,"",""]))
                            print(self.player.keys())


                    case "exit":
                        del self.player[client_ip,player]
                        status.del_player(player)
                        status.server_game_status.num_players-=1
                        client_socket.send(pickle.dumps([f'exit',]))
                        print(self.player)
                        print(f"{player} 플레이어가 나갔습니다.")


                    case _:
                        client_socket.send(pickle.dumps(f'error'))
                        print("error")
            elif len(data_ori)>=4:
                player = data_ori[-1] 
                data = data_ori[:-1]
                self.player[client_ip,player]=client_socket
                status.server_player_status[player] = data[2][player]
                status.server_game_status = data[0]
                status.server_round_status = data[1]
                print(status.server_game_status.status)
                print([status.server_player_status[player].ready for player in status.server_player_status.keys()])
                if (False not in [status.server_player_status[player].ready for player in status.server_player_status.keys()]) and len(status.server_player_status)>1 and status.server_game_status.status == "greenroom":
                    print( [status.server_player_status[player].ready for player in status.server_player_status.keys()],self.status)
                    print("게임이 시작되었습니다.")
                    status.server_game_status.status = "start"
                    status.server_game_status.players = list(status.server_player_status.keys())
                    status.server_game_status.now_turn_player = list(status.server_player_status.keys())[0]
                    card_distribution.CardDistribution()
                    round_card_shuffle.RoundCardShuffle()
                    start_resource_distribution.StartResourceDistribution()

                    status.server_game_status.next = True
                    print(status.server_game_status.now_turn_player)
                print("status.server_game_status.next:",status.server_game_status.next)
                if status.server_game_status.next:
                    status.server_game_status.next = False
                    for key,client in self.player.items():
                        print(f"데이터를 전송했습니다 : {key}")
                        client.send(pickle.dumps([status.server_game_status,status.server_round_status,status.server_player_status,"",""]))
            print(status.server_player_status.keys())
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Client_Class()
    global pprint
    pprint = main.pprint
    main.show()
    sys.exit(app.exec_())