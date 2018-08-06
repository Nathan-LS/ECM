from database.tables.base_api_one_one import *
from database.tables import *


class Char_fleet(Base, api_one_one_no_auto_pull):
    __tablename__ = 'char_fleet'

    character_id = Column(Integer, ForeignKey("tokens.for_character"), primary_key=True, nullable=False)
    fleet_id = Column(BIGINT, default=None, nullable=True)
    # squad_id = Column(Integer,default=None, nullable=True)
    wing_id = Column(BIGINT, default=None, nullable=True)

    api_ETag = Column(String, default=None, nullable=True)
    api_Expires = Column(DateTime, default=None, nullable=True)
    api_Last_Modified = Column(DateTime, default=None, nullable=True)

    object_token = relationship(tb_tokens, uselist=False, back_populates="object_char_fleet")

    def __init__(self, pilot_id: int):
        self.character_id = pilot_id

    def get_api(self, configuration):
        return swagger_client.FleetsApi(swagger_client.ApiClient(configuration))

    def get_response(self, api, token):
        return api.get_characters_character_id_fleet_with_http_info(self.character_id, datasource='tranquility',
                                                                    token=token,
                                                                    user_agent="my_test_agent",
                                                                    if_none_match=str(self.api_ETag))

    @classmethod
    def primary_key_row(cls):
        return cls.character_id
