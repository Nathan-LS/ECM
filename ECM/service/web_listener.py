from PyQt5.QtCore import *
from bottle import request
from flask import Flask, request


class web_listener(QThread):
    webApp = Flask(__name__)
    valid_callback = pyqtSignal(str)

    def __init__(self, service_module):
        super().__init__()
        self.service = service_module

    def listener_sso(self):
        auth_code = request.args.get("code")
        if auth_code:
            self.valid_callback.emit(auth_code)
            return (
                "Successfully authorized! You can safely close this window.\nPlease confirm you wish to add this character to the application back in the desktop application.")
        else:
            return ("Something went wrong when attempting to authorize. Please close this window and try again.")

    def get_callback_url(self) -> str:
        return ("http://localhost:5342/listener")  # todo dynamically change

    def run(self):
        self.webApp.route('/listener')(self.listener_sso)
        self.webApp.run(host="localhost", port=5342)
        # self.webApp.run(host="localhost", port=5342,ssl_context='adhoc')
