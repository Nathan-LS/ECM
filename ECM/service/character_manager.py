from service.service_module import *
from windows.widget_pilot_tabs import widget_pilots_tab
from PyQt5.QtCore import pyqtSignal
import requests
import os


class character_manager(QObject):
    signal_pilot_add = pyqtSignal(object)

    def __init__(self, service_module):
        super(character_manager, self).__init__()
        self.service = service_module
        assert isinstance(self.service, service.service_module.Service_Module)
        self.all_chars = {}
        self.qt_widget_pilot_view = widget_pilots_tab(parent=self, service_module=self.service, char_manager=self)
        self.__loader()

    def __loader(self):
        db: Session = self.service.get_session()
        for id in db.query(tb_tokens.for_character).all():
            self.__load_char(id.for_character)
        self.__emit_tracked()

    def __load_char(self, id):
        if not self.get_char(id):
            pilot_instance = Pilot(pilot_id=id, service_module=self.service)
            self.all_chars[pilot_instance.id] = pilot_instance

    def __emit_tracked(self):
        """emits all tracked chars. This should only be ran when creating the char manager class"""
        for pilot in self.pilots_active:
            self.signal_pilot_add.emit(pilot)

    def get_char(self, pilot_id) -> Pilot:
        return self.all_chars.get(pilot_id)

    def new_char(self, id):
        pilot_ob = self.get_char(id)
        if pilot_ob:
            pilot_ob.reload()
        else:
            self.__load_char(id)
            pilot_ob = self.get_char(id)
            if pilot_ob:
                self.signal_pilot_add.emit(self.get_char(id))

    @property
    def pilots_active(self):
        temp_list = []
        for val in self.all_chars.values():
            assert isinstance(val, Pilot)
            if val.is_tracked:
                temp_list.append(val)
        return temp_list
