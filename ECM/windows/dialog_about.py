from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui_forms.dialog_about import Ui_dialog_about
from service.service_module import *


class dialog_about(QDialog):
    def __init__(self, parent, service_object: Service_Module):
        super(dialog_about, self).__init__(parent)
        self.service = service_object
        self.ui = Ui_dialog_about()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setModal(True)
