from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_forms.add_char_dialog import Ui_add_char
from ui_forms.confirm_add_char import Ui_confirm_add_char
from ui_forms.widget_pane_char_overview import Ui_tab_overview
from ui_forms.widget_pilot_tabs import Ui_pilot_tab_widget
from service.service_module import *
from urllib.parse import quote
import webbrowser


class widget_pane_overview(QWidget):
    def __init__(self, parent, service_module, char_manager):
        super(widget_pane_overview, self).__init__(parent)
        self.service = service_module
        self.pilot_manager = char_manager
        self.ui = Ui_tab_overview()
        self.ui.setupUi(self)
        self.__load()
        self.__connects()

    def __load(self):
        self.box_layout = QVBoxLayout()
        self.ui.scrollArea.setLayout(self.box_layout)

    def __connects(self):
        self.pilot_manager.signal_pilot_add.connect(self.__slot_pilot_added)

    def __slot_pilot_added(self, pilot):
        assert isinstance(pilot, service.service_module.Pilot)
        self.box_layout.addWidget(pilot.overview_widget)


class widget_pilots_tab(QWidget):
    def __init__(self, parent, service_module, char_manager):
        super(widget_pilots_tab, self).__init__()
        self.service = service_module
        self.pilot_manager = char_manager
        assert isinstance(self.service, service.service_module.Service_Module)
        assert isinstance(self.pilot_manager, service.service_module.character_manager)
        self.ui = Ui_pilot_tab_widget()
        self.ui.setupUi(self)
        self.__load()
        self.connects()

    def __load(self):
        self.ui.pilot_tabs.addTab(
            widget_pane_overview(parent=self, service_module=self.service, char_manager=self.pilot_manager), "Overview")

    def connects(self):
        self.pilot_manager.signal_pilot_add.connect(self.__slot_pilot_added)
        # self.ui.sso_redirect.clicked.connect(self.slot_sso_open_browser)

    def __slot_pilot_added(self, pilot):
        assert isinstance(pilot, service.service_module.Pilot)
        self.ui.pilot_tabs.addTab(pilot.char_pane, pilot.name)
