from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_forms.add_char_dialog import Ui_add_char
from ui_forms.confirm_add_char import Ui_confirm_add_char
from ui_forms.widget_navigation_pane import Ui_pane_navigation
from service.service_module import *
from urllib.parse import quote
import webbrowser


class widget_pane_navigation(QWidget):
    def __init__(self, parent, service_module):
        super(widget_pane_navigation, self).__init__(parent)
        self.service = service_module
        self.ui = Ui_pane_navigation()
        self.ui.setupUi(self)
        self.connects()

    def load(self):
        pass

    def connects(self):
        pass
