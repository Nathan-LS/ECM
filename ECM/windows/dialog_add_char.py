from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_forms.add_char_dialog import Ui_add_char
from ui_forms.confirm_add_char import Ui_confirm_add_char
from ui_forms.widget_scope_sso import Ui_scopes_sso
from service.service_module import *
from urllib.parse import quote
import webbrowser


class ScopesSSO_List(QWidget):
    def __init__(self, parent, service_module):
        super(ScopesSSO_List, self).__init__(parent)
        self.service = service_module
        self.ui = Ui_scopes_sso()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.load()
        self.connects()

    def load(self):
        def helper(list_get_function, list_widget):
            for i in list_get_function():
                item = QListWidgetItem()
                item.setText(i.scope)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                if i.used:
                    item.setCheckState(Qt.Checked)
                else:
                    item.setCheckState(Qt.Unchecked)
                list_widget.addItem(item)

        helper(self.service.settings.get_read_scopes, self.ui.read_scopes_list)
        helper(self.service.settings.get_write_scopes, self.ui.write_scopes_list)

    def connects(self):
        self.ui.sso_redirect.clicked.connect(self.slot_sso_open_browser)

    def slot_sso_open_browser(self):
        def helper(list_widget) -> str:
            scope_str = ""
            for index in range(list_widget.count()):
                if list_widget.item(index).checkState() == Qt.Checked:
                    scope_str += (list_widget.item(index).text() + " ")
            return scope_str

        callback = self.service.callback_listener.get_callback_url()
        client_id = self.service.settings.get_client_id()
        scopes = quote(((helper(self.ui.read_scopes_list) + helper(self.ui.write_scopes_list)).strip()).lower())
        if client_id:
            url = "https://login.eveonline.com/oauth/authorize?response_type=code&redirect_uri={cb}&client_id={cid}&scope={scopes}".format(
                cb=callback, cid=client_id, scopes=scopes)
            webbrowser.open(url)
        else:
            error_popup(parent=self, error_text="You must define a valid client ID and client secret")


class error_popup(QMessageBox):
    def __init__(self, parent, error_text):
        super(error_popup, self).__init__(parent)
        self.setIcon(QMessageBox.Critical)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setInformativeText(error_text)
        self.exec()


class dialog_char_select(QDialog):
    def __init__(self, parent, service_object: Service_Module, auth_token):
        super(dialog_char_select, self).__init__(parent)
        self.service = service_object
        self.ui = Ui_confirm_add_char()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setModal(True)
        self.connects()

        self.c_id = None
        self.extract_details(auth_token)

    def connects(self):
        self.ui.confirm_add_button.clicked.connect(self.slot_confirm_add)
        self.ui.cancel_button.clicked.connect(self.slot_cancel_add)

    def extract_details(self, auth_token):
        try:
            __row: tb_tokens = tb_tokens.get_row_from_auth(auth_token, self.service)
            if __row is not None:
                self.service.get_session().merge(__row)
                pilot_image = self.service.images.get_pilot(__row.object_character.character_id, pull_new=True)
                corp_image = self.service.images.get_corp(__row.object_character.object_corp.corporation_id,
                                                          pull_new=True)
                self.ui.pilot_image.setScaledContents(True)
                self.ui.pilot_image.setPixmap(pilot_image)
                self.ui.corp_image.setScaledContents(True)
                self.ui.corp_image.setPixmap(corp_image)
                self.ui.pilot_name.setText(__row.object_character.name)
                self.c_id = __row.object_character.character_id
                self.slot_show_ok()
            else:
                self.slot_error()
        except Exception as ex:
            error_popup(self, "Something went wrong when attempting to get a token\n\n{}".format(ex))

    def slot_confirm_add(self):
        try:
            self.service.get_session().commit()
            self.service.characters.new_char(self.c_id)
        except Exception as ex:
            self.service.get_session().rollback()
            error_popup(self, "Something went wrong when attempting to add the char\n'{}'".format(ex))
        self.close()

    def slot_cancel_add(self):
        self.service.get_session().rollback()
        self.close()

    def slot_show_ok(self):
        self.exec()

    def slot_error(self):
        error_popup(self, "Something went wrong when attempting to get a token")
        self.close()


class dialog_add_char(QDialog):
    def __init__(self, parent, service_ob: Service_Module):
        super(dialog_add_char, self).__init__(parent)
        self.service = service_ob
        self.ui = Ui_add_char()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setModal(True)

        self.load()
        self.connects()

    def connects(self):
        self.ui.save_dev.clicked.connect(self.slot_save_dev_details)
        self.service.callback_listener.valid_callback.connect(self.slot_callback)

    def load(self):  # load previous values if they exit
        self.scopes = ScopesSSO_List(self, self.service)
        self.ui.load_sso.addWidget(self.scopes)
        self.ui.client_id_input.setText(self.service.settings.get_client_id())
        self.ui.secret_key_input.setText(self.service.settings.get_secret_key())
        if self.ui.client_id_input.text() and self.ui.secret_key_input.text():
            self.state_login_mode()
        else:
            self.state_edit_mode()

    def slot_save_dev_details(self):
        if self.ui.client_id_input.text() and self.ui.secret_key_input.text() and not self.scopes.isEnabled():
            self.state_login_mode()
        elif self.scopes.isEnabled():
            self.state_edit_mode()
        else:
            error_popup(parent=self, error_text="You must enter both a Developer Application client_id and secret_key")

    def state_login_mode(self):
        self.service.settings.set_client_id(self.ui.client_id_input.text())
        self.service.settings.set_secret_key(self.ui.secret_key_input.text())
        self.scopes.setEnabled(True)
        self.ui.client_id_input.setEnabled(False)
        self.ui.secret_key_input.setEnabled(False)
        self.ui.save_dev.setText("Edit Dev Details")

    def state_edit_mode(self):
        self.scopes.setEnabled(False)
        self.ui.client_id_input.setEnabled(True)
        self.ui.secret_key_input.setEnabled(True)
        self.ui.save_dev.setText("Save Details")

    def slot_callback(self, code):
        confirm = dialog_char_select(parent=self, service_object=self.service, auth_token=code)
