from PyQt5.QtWidgets import *
from ui_forms.main import Ui_MainWindow
from service.service_module import *
from windows.dialog_add_char import dialog_add_char
from windows.widget_pane_navigation import widget_pane_navigation
from windows.dialog_about import dialog_about
from functools import partial


class window_Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.service = Service_Module()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.panes()
        self.ui.statusbar.setStyleSheet("background-color: rgb(218, 218, 218);")
        self.status_bar_clock = QLabel()
        self.ui.statusbar.addPermanentWidget(self.status_bar_clock)
        self.__load()
        self.connects()

    def panes(self):
        self.character_view = self.service.characters.qt_widget_pilot_view
        self.navigation_view = widget_pane_navigation(parent=None, service_module=self.service)
        self.ui.stacked_pages.addWidget(self.character_view)
        self.ui.stacked_pages.addWidget(self.navigation_view)
        self.ui.stacked_pages.setCurrentWidget(self.character_view)

    def __load(self):
        self.service.scheduler.tasks_time.add_task(self.__slot_updateStatusBar,
                                                   self.service.settings.get_status_bar_clock_online_count(),
                                                   run_now=True)

    def connects(self):
        self.ui.actionReset_Settings.triggered.connect(self.service.settings.reset_settings)
        self.ui.actionSave_Settings.triggered.connect(self.service.settings.save)
        self.ui.actionAdd_character.triggered.connect(self.slot_add_char)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionAPI_Tester.triggered.connect(self.slot_apitest)
        self.ui.actionAbout.triggered.connect(self.slot_about)
        self.ui.actionCharacter.triggered.connect(partial(self.slot_change_pane, self.character_view))
        self.ui.actionNavigation.triggered.connect(partial(self.slot_change_pane, self.navigation_view))

    def __slot_updateStatusBar(self, time_now):
        api = swagger_client.StatusApi()
        api.api_client.set_default_header('User-Agent', self.service.settings.get_user_agent())
        api.api_client.host = self.service.settings.get_api_host()
        online_count = 0
        status = "Unknown"
        time_str = "{}:{}".format(str(time_now.hour).zfill(2), str(time_now.minute).zfill(2))
        try:
            response = api.get_status()
            online_count = response.players
            if online_count != 0:
                status = "Online"
            self.service.logger.status("api playercount ok")
        except Exception as ex:
            print(ex)
            self.service.logger.error("api playercount exception")
        self.status_bar_clock.setText(
            "EVE Time: {} | Tranquility Server {} ({} Pilots)".format(time_str, status, online_count))

    def slot_apitest(self):
        raise NotImplementedError
        # suite_test(self)

    def slot_add_char(self, pane):
        __ob_dialog_add_char = dialog_add_char(parent=self, service_ob=self.service)
        __ob_dialog_add_char.exec()

    def slot_about(self):
        __about = dialog_about(parent=self, service_object=self.service)
        __about.exec()

    def slot_change_pane(self, pane_widget: QWidget):
        self.ui.stacked_pages.setCurrentWidget(pane_widget)

    def show(self):
        super().show()
