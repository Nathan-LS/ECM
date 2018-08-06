from service.service_module import *
import service.service_module
import datetime


class logger(QObject):

    def __init__(self, service_module):
        super(logger, self).__init__()
        self.service = service_module
        assert isinstance(self.service, service.service_module.Service_Module)

    def error(self, message: str):
        newlog = tb_logs(time=datetime.datetime.utcnow(), type="error", message=message)
        self.__new(newlog)

    def warning(self, message: str):
        newlog = tb_logs(time=datetime.datetime.utcnow(), type="warning", message=message)
        self.__new(newlog)

    def status(self, message: str):
        newlog = tb_logs(time=datetime.datetime.utcnow(), type="status", message=message)
        self.__new(newlog)

    def __new(self, row):
        self.service.get_session().add(row)
        self.__save()

    def __save(self):
        self.service.get_session().commit()
        self.service.close_session()
