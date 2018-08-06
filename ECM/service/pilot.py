from service.service_module import *
from service.scheduler import task_container
from PyQt5.QtCore import pyqtSignal
from windows.panes.char_view import widget_char_view
from windows.panes.overview_char import widget_char_overview
import datetime
from threading import Lock
from PyQt5 import QtCore


class Pilot(QObject):
    signal_changed_table_characters = pyqtSignal()
    signal_changed_table_Char_attributes = pyqtSignal()
    signal_changed_table_Char_location = pyqtSignal()
    signal_changed_table_Char_fatigue = pyqtSignal()
    signal_changed_table_Char_fleet = pyqtSignal()
    signal_changed_table_Char_skills_info = pyqtSignal()

    def __init__(self, pilot_id, service_module):
        super(Pilot, self).__init__()
        self.id_ = pilot_id
        self.service = service_module
        assert isinstance(self.service, service.service_module.Service_Module)
        self.scheduler = task_container(thread_count=16, auto_sort=True)
        self.service.scheduler.tasks_api.add_task(self.scheduler.run_tasks, seconds_interval=1)
        self.__load_rows()
        self.__connects()
        self.__make_tasks()
        self.token_lock = Lock()
        self.char_pane = widget_char_view(parent=None, char_object=self, service_module=self.service)
        self.overview_widget = widget_char_overview(parent=None, char_object=self, service_module=self.service)
        self.__emit_all()

    def __make_tasks(self):
        self.scheduler.clear_tasks()
        self.scheduler.add_task(self.__api_get_skill_attributes, seconds_interval=3600, run_now=True)
        self.scheduler.add_task(self.__api_get_fatigue, seconds_interval=300, run_now=True)
        self.scheduler.add_task(self.__api_get_location, seconds_interval=600, run_now=True)
        self.scheduler.add_task(self.__api_get_skills, seconds_interval=3600, run_now=True)
        self.scheduler.add_task(self.__api_get_fleet_id, seconds_interval=60, run_now=True)
        self.scheduler.add_task(self.__api_get_char_public, seconds_interval=3600, run_now=True)

    def __load_rows(self):
        # self.cache_table_characters = self.table_characters
        # self.cache_table_Char_attributes = self.table_Char_attributes
        # self.cache_table_Char_location = self.table_Char_location
        # self.cache_table_Char_fatigue = self.table_Char_fatigue
        # self.cache_table_Char_fleet = self.table_Char_fatigue
        # self.cache_table_Char_skills_info = self.table_Char_skills_info
        self.cache_scopes = self.__scopes

    def __connects(self):
        pass

    def __emit_all(self):
        self.signal_changed_table_characters.emit()
        self.signal_changed_table_Char_attributes.emit()
        self.signal_changed_table_Char_location.emit()
        self.signal_changed_table_Char_fatigue.emit()
        self.signal_changed_table_Char_fleet.emit()
        self.signal_changed_table_Char_skills_info.emit()

    def reload(self):
        self.__load_rows()
        self.__make_tasks()
        self.__emit_all()

    def __api_get(self, task, row_return, signal, scope_list=list()):
        if not self.__has_scopes(scope_list):
            self.scheduler.remove_task(task)
            return
        token = self.__token
        if token:
            __status = row_return.api_populate(token)
            if __status == 200:
                try:
                    row_return.api_populate_fk_objects(self.service)
                    # self.service.get_session().merge(row_return)
                    self.service.get_session().commit()
                    signal.emit()
                except Exception as ex:
                    pass
            elif __status == 304:  # do nothing
                pass
            elif __status == 403:
                self.scheduler.remove_task(task)
            elif __status == 404:
                pass
            elif __status == 420:  # error limited
                self.scheduler.retry_task(task, 30)
            elif __status >= 500:  # server error
                self.scheduler.retry_task(task, 25)
            else:
                self.scheduler.retry_task(task, 5)
            self.service.close_session()

    def __api_get_char_public(self):
        self.__api_get(self.__api_get_char_public, self.table_characters, self.signal_changed_table_characters)

    def __api_get_skill_attributes(self):
        __scopes = ["esi-skills.read_skills.v1"]
        self.__api_get(self.__api_get_skill_attributes, self.table_Char_attributes,
                       self.signal_changed_table_Char_attributes, __scopes)

    def __api_get_fatigue(self):
        __scopes = ["esi-characters.read_fatigue.v1"]
        self.__api_get(self.__api_get_fatigue, self.table_Char_fatigue, self.signal_changed_table_Char_fatigue,
                       __scopes)

    def __api_get_location(self):
        __scopes = ["esi-location.read_location.v1"]
        self.__api_get(self.__api_get_location, self.table_Char_location, self.signal_changed_table_Char_location,
                       __scopes)

    def __api_get_skills(self):
        __scopes = ["esi-skills.read_skills.v1"]
        self.__api_get(self.__api_get_skills, self.table_Char_skills_info, self.signal_changed_table_Char_skills_info,
                       __scopes)

    def __api_get_fleet_id(self):
        __scopes = ["esi-fleets.read_fleet.v1"]
        self.__api_get(self.__api_get_fleet_id, self.table_Char_fleet, self.signal_changed_table_Char_fleet, __scopes)

    @property
    def is_tracked(self):
        return True  # todo for now

    @property
    def __scopes(self):
        return [i.scope for i in tb_token_scopes.get_row(self.id, self.service)]

    @property
    def table_characters(self) -> tb_characters:
        return tb_characters.get_row(self.id, self.service)

    @property
    def table_token(self) -> tb_tokens:
        return tb_tokens.get_row(self.id, self.service)

    @property
    def table_Char_attributes(self) -> tb_attributes:
        return tb_attributes.get_row(self.id, self.service)

    @property
    def table_Char_fatigue(self):
        return tb_fatigue.get_row(self.id, self.service)

    @property
    def table_Char_location(self) -> tb_locations:
        return tb_locations.get_row(self.id, self.service)

    @property
    def table_Char_skills_info(self):
        return tb_skills_info.get_row(self.id, self.service)

    @property
    def table_Char_fleet(self):
        return tb_fleet.get_row(self.id, self.service)

    @property
    def __token(self):
        with self.token_lock:
            try:
                token_ob = self.table_token
                token = token_ob.get_token(self.service)
                self.service.get_session().merge(token_ob)
                self.service.get_session().commit()
                return token
            except:
                self.service.get_session().rollback()
                return None

    def __has_scopes(self, scope_list):
        return set(scope_list).issubset(self.cache_scopes)

    @property
    def id(self):
        return self.id_

    @property
    def name(self):
        return self.table_characters.name

    # @property
    # def accrued_remap_cooldown_date(self):
    #     return self.cache_table_Char_attributes.accrued_remap_cooldown_date
    #
    # @property
    # def bonus_remaps(self):
    #     return self.cache_table_Char_attributes.bonus_remaps

    # @property
    # def corporation(self):
    #     try:
    #         return self.cache_table_characters.object_corp.name
    #     except:
    #         return None
    #
    # @property
    # def alliance(self):
    #     try:
    #         return self.cache_table_characters.object_alliance.name
    #     except:
    #         return None
    #
    # @property
    # def charisma(self):
    #     return self.cache_table_Char_attributes.charisma
    #
    # @property
    # def intelligence(self):
    #     return self.cache_table_Char_attributes.intelligence
    #
    # @property
    # def last_remap_date(self):
    #     return self.cache_table_Char_attributes.last_remap_date
    #
    # @property
    # def memory(self):
    #     return self.cache_table_Char_attributes.memory
    #
    # @property
    # def perception(self):
    #     return self.cache_table_Char_attributes.perception
    #
    # @property
    # def willpower(self):
    #     return self.cache_table_Char_attributes.willpower
    #
    # @property
    # def location_system_name(self):
    #     try:
    #         return self.table_Char_location.object_system.name
    #     except:
    #         return None
    #
    # @property
    # def location_region_name(self):
    #     try:
    #         return self.table_Char_location.object_system.object_constellation.object_region.name
    #     except:
    #         return None
    #
    # @property
    # def total_sp(self):
    #     return self.table_Char_skills_info.total_sp
    #
    # @property
    # def free_sp(self):
    #     return self.table_Char_skills_info.unallocated_sp
