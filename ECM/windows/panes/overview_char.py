from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_forms.widget_overview_char import Ui_widget_overview_button
from service.service_module import *
from urllib.parse import quote
import webbrowser
import datetime
import time


class widget_char_overview(QWidget):
    def __init__(self, parent=None, char_object=None, service_module=None):
        super(widget_char_overview, self).__init__(parent)
        self.service = service_module
        self.pilot = char_object
        assert isinstance(self.service, service.service_module.Service_Module)
        assert isinstance(self.pilot, service.service_module.Pilot)
        self.ui = Ui_widget_overview_button()
        self.ui.setupUi(self)
        self.__load()
        self.connects()

    def __load(self):
        self.__counter_total_sp = dynamic_sp_counter()
        self.service.scheduler.tasks_time.add_task(self.__slot_update_timers, seconds_interval=1)

    def connects(self):
        self.pilot.signal_changed_table_characters.connect(self.__slot_draw_char_public)
        self.pilot.signal_changed_table_Char_skills_info.connect(self.__slot_draw_skill_info)

    def __slot_update_timers(self, time_now):
        self.ui.text_sp.setText(str(self.__counter_total_sp.update_time(time_now)) + " SP")

    def __slot_draw_char_public(self):
        return
        self.ui.text_name.setText(self.pilot.name)
        self.ui.pilot_image.setPixmap(self.service.images.get_pilot(self.pilot.id))

    def __slot_draw_skill_info(self):
        return
        self.service.get_session().expire_all()
        self.__counter_total_sp = dynamic_sp_counter(start_time=datetime.datetime.utcnow(),
                                                     starting_sp=self.pilot.total_sp, sp_hr=2610)
