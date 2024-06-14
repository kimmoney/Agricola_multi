from data.py.def_list import *
# sys.excepthook = custom_exception_handler
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
        self.setting = {"background_media":False,"event_media":True,"name":""}
        self.change_main_page = lambda after_page: change_stacked_page(self,self.main_Stacked_Widget, after_page)
        self.timer_close,self.timer_open = QTimer(self),QTimer(self)

        self.btn_start.clicked.connect(lambda:self.change_main_page("sign_up"))

        self.btn_sign_up_confirm.clicked.connect(self.func_sign_up)
        self.btn_sign_up_exit.clicked.connect(lambda:self.change_main_page("start_page"))

        self.btn_main_greenroom_near.clicked.connect(lambda:self.change_main_page("greenroom_near"))
        self.btn_main_greenroom_far.clicked.connect(lambda:self.change_main_page("greenroom_far"))
        self.btn_main_setting.clicked.connect(self.open_setting)

        self.back_near.clicked.connect(lambda:self.change_main_page("menu"))
        self.back_far. clicked.connect(lambda:self.change_main_page("menu"))

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


















def Start_Client():
    app = QApplication(sys.argv)
    mainWin = Client_Class()
    global pprint
    pprint = mainWin.pprint
    mainWin.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    Start_Client()