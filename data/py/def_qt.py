from def_list import *

def change_main_stacked(self):
        self.update_state_of_all()
        currentWidget = self.stackedWidget.currentWidget().objectName()
        # if index == 0:self.stackedWidget.setCurrentIndex(1)
        # else:self.stackedWidget.setCurrentIndex(0)
        
        if currentWidget == "round_page":self.change_stacked_page("personal_page")
        else:self.change_stacked_page("round_page")


def change_stacked_page(self, stacked_Widget, after_page):
    after_page = getattr(self, after_page)
    if stacked_Widget.currentWidget() != after_page:
        self.speed = 13
        self.total_timer_count = 10
        if not self.timer_close.isActive() and not self.timer_open.isActive():
            # 이걸로 속도 조절 낮을수록 빠름
            self.opacity_effect = QGraphicsOpacityEffect(stacked_Widget.currentWidget())
            self.opacity_effect_after = QGraphicsOpacityEffect(after_page)
            self.opacity_effect_after.setOpacity(0)
            self.timer_close = QTimer(self)
            self.timer_open = QTimer(self)
            self.current_timer_count = 0
            self.timer_open.stop()
            self.timer_close.stop()
            self.timer_close.timeout.connect(lambda : process_timer_close(self,after_page))
            self.timer_close.start(self.speed)
            self.timer_open.timeout.connect(lambda : process_timer_open(self,after_page))
            

        def process_timer_close(self,after_page):
            self.opacity_effect.setOpacity(1-0.1*self.current_timer_count)
            stacked_Widget.currentWidget().setGraphicsEffect(self.opacity_effect)
            self.current_timer_count += 1
            if self.current_timer_count == self.total_timer_count:
                self.opacity_effect_after.setOpacity(0)
                stacked_Widget.setCurrentWidget(after_page)
                self.opacity_effect.setOpacity(1)
                while not after_page.isVisible():
                    pass
                # self.title.setText(title)
                self.timer_open.start(self.speed)
                self.timer_close.stop()
                self.opacity_effect_after.setOpacity(1)
        def process_timer_open(self,after_page):
            self.opacity_effect_after.setOpacity(1-0.1*self.current_timer_count)
            after_page.setGraphicsEffect(self.opacity_effect_after)
            self.current_timer_count -= 1
            if self.current_timer_count == 0:
                self.timer_open.stop()



class Setting(QDialog, setting_ui):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.setting = parent.setting
        self.setWindowFlags(Qt.FramelessWindowHint |self.windowFlags() )
        self.background_media.setChecked(self.setting["background_media"])
        self.event_media.setChecked(self.setting["background_media"])

        self.close.clicked.connect(self.accept)
        self.background_media.clicked.connect(self.background_setting)
        self.event_media.clicked.connect(self.background_setting)


    def background_setting(self):
        self.setting["background_media"] = self.background_media.isChecked()
        self.parent.set_music()
    def event_setting(self):
        self.setting["event_media"] = self.event_media.isChecked()
        self.parent.set_music()

        
class Log_viewer(QDialog,log_viewer_ui):
    def __init__(self,parent):
        super().__init__()  # 부모 클래스의 __init__ 함수 호출
        self.setupUi(self)
        self.parent = parent
        self.setWindowFlags(Qt.FramelessWindowHint )
        self.setWindowFlags(Qt.FramelessWindowHint |self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.log.setText("이 곳은 로그를 표기하는 곳입니다.")
        self.timer = QTimer()
        self.hide()
        
    def showEvent(self,event):
        parent_rect = self.parent.geometry()
        dialog_rect = self.geometry()
        x = parent_rect.left() + (parent_rect.width() - dialog_rect.width()) / 2
        y = parent_rect.top() + (parent_rect.height() - dialog_rect.height()) / 2

        # 다이얼로그를 계산된 좌표로 이동
        self.move(int(x), int(y))
    def logging(self,text,time=500):
        self.timer.stop()
        self.log.setText(text)
        self.show()
        self.timer.timeout.connect(self.hide)
        self.timer.start(500) 
    