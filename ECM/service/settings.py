from service.service_module import *


class settings(QObject):

    def __init__(self, service_module):
        super(settings, self).__init__()
        self.service = service_module
        assert isinstance(self.service, service.service_module.Service_Module)
        self.cached_data = self.__new()

    def get_status_bar_clock_online_count(self) -> int:
        return int(self.cached_data.status_bar_clock_online_count)

    def set_get_status_bar_clock_online_count(self, seconds: int):
        self.__data.status_bar_clock_online_count = seconds
        self.__save()

    def set_client_id(self, id: str):
        self.__data.client_id = id
        self.__save()

    def set_secret_key(self, key: str):
        self.__data.secret_key = key
        self.__save()

    def get_api_host(self) -> str:
        return self.cached_data.API_Host

    def get_user_agent(self) -> str:
        return self.cached_data.User_Agent

    def get_client_id(self) -> str:
        return self.cached_data.client_id

    def get_secret_key(self) -> str:
        return self.cached_data.secret_key

    def get_read_scopes(self):
        ses: Session = self.service.get_session()
        items = ses.query(tb_scopes).filter(tb_scopes.read_write == "read").order_by(tb_scopes.scope).all()
        self.service.close_session()
        return items

    def get_write_scopes(self):
        ses: Session = self.service.get_session()
        items = ses.query(tb_scopes).filter(tb_scopes.read_write == "write").order_by(tb_scopes.scope).all()
        self.service.close_session()
        return items

    def reset_settings(self):
        self.service.get_session().delete(self.__data)
        self.__save()
        self.__new()

    def save(self):
        self.__save()

    def __save(self):
        self.service.get_session().commit()
        self.__recache()
        self.service.close_session()

    @property
    def __data(self):
        return self.service.get_session().query(tb_settings).one()

    def __new(self):  # creates a new settings row if none exists or reloads the data
        try:
            data = self.__data
        except NoResultFound:
            data = tb_settings()  # make new row
            self.service.get_session().add(data)
            self.__save()
        return data

    def __recache(self):
        self.cached_data = self.__new()
