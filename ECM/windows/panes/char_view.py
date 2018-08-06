from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_forms.widget_pane_char_view import Ui_pane_char_view
from service.service_module import *
from urllib.parse import quote
import webbrowser
import datetime
import time
from PyQt5 import QtCore


class widget_char_view(QWidget):
    def __init__(self, parent=None, char_object=None, service_module=None):
        super(widget_char_view, self).__init__(parent)
        self.service = service_module
        self.pilot = char_object
        assert isinstance(self.service, service.service_module.Service_Module)
        assert isinstance(self.pilot, service.service_module.Pilot)
        self.ui = Ui_pane_char_view()
        self.ui.setupUi(self)
        self.__load()
        self.connects()

    def __load(self):
        self.__counter_total_sp = dynamic_sp_counter()
        self.service.scheduler.tasks_time.add_task(self.__slot_update_timers, seconds_interval=1)

    def connects(self):
        self.pilot.signal_changed_table_characters.connect(self.__slot_draw_char_public)
        self.pilot.signal_changed_table_Char_location.connect(self.__slot_draw_char_location)
        self.pilot.signal_changed_table_Char_attributes.connect(self.__slot_draw_char_attributes)
        self.pilot.signal_changed_table_Char_skills_info.connect(self.__slot_draw_skill_info)

    def __slot_update_timers(self, time_now):
        self.ui.text_api_nextupdate_countdown.setText(str(dynamic_countdown(self.pilot.scheduler.next_task, time_now)))
        self.ui.text_total_sp.setText(str(self.__counter_total_sp.update_time(time_now)))

    def __slot_draw_char_public(self):
        tb: tb_characters = self.pilot.table_characters
        self.ui.text_pilot_name.setText(str(tb.name))
        self.ui.pilot_image.setPixmap(self.service.images.get_pilot(self.pilot.id))
        self.ui.text_corp.setText(str(tb.object_corp.name) if tb.object_corp else "")
        self.ui.text_alliance.setText(str(tb.object_alliance.name) if tb.object_alliance else "")
        self.ui.text_birthday.setText(str(tb.birthday))
        self.ui.text_sec_status.setText(str(tb.security_status))

    def __slot_draw_char_location(self):
        tb: tb_locations = self.pilot.table_Char_location
        __loc_system = "{}".format(str(tb.object_system.name) if tb.object_system else "")
        # __loc_region = "{}".format(str(tb.object_system.object_region.name)if tb.object_system and tb.object_system.object_constellation.object_region else "")
        self.ui.text_located_at.setText("{} ({})".format(__loc_system, ""))

    def __slot_draw_char_attributes(self):
        tb: tb_attributes = self.pilot.table_Char_attributes
        self.ui.text_attributes_charisma.setText(str(tb.charisma))
        self.ui.text_attributes_intel.setText(str(tb.intelligence))
        self.ui.text_attributes_memory.setText(str(tb.memory))
        self.ui.text_attributes_perception.setText(str(tb.perception))
        self.ui.text_attributes_willpower.setText(str(tb.willpower))
        self.ui.text_bonus_remap_count.setText(str(tb.bonus_remaps))
        self.ui.text_next_remap_datetime.setText(str(tb.accrued_remap_cooldown_date))

    def __slot_draw_skill_info(self):
        return
        self.service.get_session().expire_all()
        self.ui.text_freeSP.setText(str(self.pilot.free_sp))
        self.__counter_total_sp = dynamic_sp_counter(start_time=datetime.datetime.utcnow(),
                                                     starting_sp=self.pilot.total_sp, sp_hr=2610)
