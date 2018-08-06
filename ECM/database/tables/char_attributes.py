from database.tables.base_api_one_one import *
from database.tables import *


class Char_attributes(Base, api_one_one_no_auto_pull):
    __tablename__ = 'char_attributes'

    character_id = Column(Integer, ForeignKey("tokens.for_character"), primary_key=True, nullable=False)
    accrued_remap_cooldown_date = Column(DateTime, default=None, nullable=True)
    last_remap_date = Column(DateTime, default=None, nullable=True)
    bonus_remaps = Column(Integer, default=0, nullable=False)
    charisma = Column(Integer, default=0, nullable=False)
    intelligence = Column(Integer, default=0, nullable=False)
    memory = Column(Integer, default=0, nullable=False)
    perception = Column(Integer, default=0, nullable=False)
    willpower = Column(Integer, default=0, nullable=False)

    api_ETag = Column(String, default=None, nullable=True)
    api_Expires = Column(DateTime, default=None, nullable=True)
    api_Last_Modified = Column(DateTime, default=None, nullable=True)

    object_token = relationship("Tokens", uselist=False, back_populates="object_char_attributes")

    def __init__(self, pilot_id: int):
        self.character_id = pilot_id

    def get_api(self, configuration):
        return swagger_client.SkillsApi(swagger_client.ApiClient(configuration))

    def get_response(self, api, token):
        return api.get_characters_character_id_attributes_with_http_info(self.character_id, datasource='tranquility',
                                                                         token=token, user_agent="my_test_agent",
                                                                         if_none_match=str(self.api_ETag))

    @classmethod
    def primary_key_row(cls):
        return cls.character_id
