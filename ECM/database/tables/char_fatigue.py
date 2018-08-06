from database.tables.base_api_one_one import *
from database.tables import *


class Char_fatigue(Base, api_one_one_no_auto_pull):
    __tablename__ = 'char_fatigue'

    character_id = Column(Integer, ForeignKey("tokens.for_character"), primary_key=True, nullable=False)
    jump_fatigue_expire_date = Column(DateTime, default=None, nullable=True)
    last_jump_date = Column(DateTime, default=None, nullable=True)
    last_update_date = Column(DateTime, default=None, nullable=True)

    api_ETag = Column(String, default=None, nullable=True)
    api_Expires = Column(DateTime, default=None, nullable=True)
    api_Last_Modified = Column(DateTime, default=None, nullable=True)

    object_token = relationship("Tokens", uselist=False, back_populates="object_char_fatigue")

    def __init__(self, pilot_id: int):
        self.character_id = pilot_id

    def get_api(self, configuration):
        return swagger_client.CharacterApi(swagger_client.ApiClient(configuration))

    def get_response(self, api, token):
        return api.get_characters_character_id_fatigue_with_http_info(self.character_id, datasource='tranquility',
                                                                      token=token,
                                                                      user_agent="my_test_agent",
                                                                      if_none_match=str(self.api_ETag))

    @classmethod
    def primary_key_row(cls):
        return cls.character_id
