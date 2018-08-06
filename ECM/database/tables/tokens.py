import requests
import json
from requests.auth import HTTPBasicAuth
from database.tables.base_api_one_one import *
from database.tables import *


class Tokens(Base, api_one_to_one):
    __tablename__ = 'tokens'

    for_character = Column(Integer, ForeignKey("characters.character_id"), primary_key=True)
    token = Column(String, default=None)
    refresh_token = Column(String, default=None)
    last_update = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)

    object_character = relationship("Characters", uselist=False, back_populates="object_token")
    object_char_attributes = relationship("Char_attributes", uselist=False, cascade="delete",
                                          back_populates="object_token")
    object_char_fatigue = relationship("Char_fatigue", uselist=False, cascade="delete", back_populates="object_token")
    object_char_fleet = relationship("Char_fleet", uselist=False, cascade="delete", back_populates="object_token")
    object_char_location = relationship("Char_location", uselist=False, cascade="delete", back_populates="object_token")
    object_char_skills = relationship("Char_skills_info", uselist=False, cascade="delete",
                                      back_populates="object_token")
    object_token_scopes = relationship("Token_scopes", uselist=True, cascade="delete", back_populates="object_token")

    def __init__(self, pilot_id):
        self.for_character = pilot_id
        self.last_update = datetime.datetime.utcnow()

    def api_populate_fk_objects(self, service_module):
        if self.for_character is not None:
            self.object_character = tb_characters.get_row(self.for_character, service_module)

    def get_token(self, service_module):
        if self.refresh_token is None:  # there is no refresh token, this character is blank or tokens have been revoked
            return None
        elif datetime.datetime.utcnow() < self.last_update + datetime.timedelta(minutes=15) and self.token is not None:
            return self.token
        else:
            url = "https://login.eveonline.com/oauth/token"
            auth_header = (
                HTTPBasicAuth(service_module.settings.get_client_id(), service_module.settings.get_secret_key()))
            headers = {"Content-Type": "application/json", "User-Agent": service_module.settings.get_user_agent()}
            payload = {"grant_type": "refresh_token", "refresh_token": self.refresh_token}
            try:
                response = requests.post(url=url, auth=auth_header, data=json.dumps(payload), headers=headers)
                if response.status_code == 200:
                    self.token = response.json().get("access_token")
                    self.refresh_token = response.json().get("refresh_token")
                    self.last_update = datetime.datetime.utcnow()
                    return self.token
                elif response.status_code == 400:
                    self.token, self.refresh_token, self.last_update = None, None, datetime.datetime.utcnow()
                    return None
                else:
                    return None
            except:
                return None

    @classmethod
    def primary_key_row(cls):
        return cls.for_character  # pilot_id

    @staticmethod
    def get_token_from_auth(authorization_code, service_module):
        url = "https://login.eveonline.com/oauth/token"
        auth_header = (HTTPBasicAuth(service_module.settings.get_client_id(), service_module.settings.get_secret_key()))
        headers = {"Content-Type": "application/json", "User-Agent": service_module.settings.get_user_agent()}
        payload = {"grant_type": "authorization_code", "code": authorization_code}
        try:
            response = requests.post(url=url, auth=auth_header, data=json.dumps(payload), headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as ex:
            print(ex)

    @staticmethod
    def get_verify(token, service_module):
        url = "https://login.eveonline.com/oauth/verify"
        headers = {"Authorization": "Bearer {}".format(token), "Content-Type": "application/json",
                   "User-Agent": service_module.settings.get_user_agent()}
        try:
            response = requests.get(url=url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as ex:
            print(ex)
            return None

    @classmethod
    def get_row_from_auth(cls, auth_token, service_module: service):
        if auth_token is not None:
            response = cls.get_token_from_auth(auth_token, service_module)
            if response:
                c_token = response.get("access_token")
                c_refresh_token = response.get("refresh_token")
                if c_token and c_refresh_token:
                    response = cls.get_verify(c_token, service_module)
                    c_id = response.get("CharacterID")
                    __row = cls.get_row(c_id, service_module)
                    __row.token = c_token
                    __row.refresh_token = c_refresh_token
                    __row.last_update = datetime.datetime.utcnow()
                    service_module.get_session().query(tb_token_scopes).filter(
                        tb_token_scopes.pilot_id == __row.for_character).delete()
                    for i in response.get("Scopes").split(' '):
                        scope = tb_scopes.get_row(i, service_module)
                        if scope is not None:
                            try:
                                service_module.get_session().merge(tb_token_scopes(__row, scope))
                            except Exception as ex:
                                print(ex)
                    return __row
        return None
