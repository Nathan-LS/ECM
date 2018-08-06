from database.tables.base_api_one_one import *
from database.tables import *


class Characters(Base, api_one_to_one):
    __tablename__ = 'characters'

    character_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, default=None, nullable=True)
    corporation_id = Column(Integer, ForeignKey("corporations.corporation_id"), nullable=False)
    alliance_id = Column(Integer, ForeignKey("alliances.alliance_id"), nullable=True)
    birthday = Column(DateTime, default=None, nullable=True)
    description = Column(String, default=None, nullable=True)
    security_status = Column(Float, default=0.0, nullable=True)

    gender = Column(String, default=None, nullable=True)
    faction_id = Column(String, default=None, nullable=True)
    race_id = Column(Integer, default=None, nullable=True)
    bloodline_id = Column(Integer, default=None, nullable=True)
    ancestry_id = Column(Integer, default=None, nullable=True)

    api_ETag = Column(String, default=None, nullable=True)
    api_Expires = Column(DateTime, default=None, nullable=True)
    api_Last_Modified = Column(DateTime, default=None, nullable=True)

    object_token = relationship("Tokens", uselist=False, back_populates="object_character")
    object_corp = relationship("Corporations", uselist=False, back_populates="object_characters")
    object_alliance = relationship("Alliances", uselist=False, back_populates="object_characters")

    def __init__(self, pilot_id: int):
        self.character_id = pilot_id

    def api_populate_fk_objects(self, service_module):
        if self.corporation_id is not None:
            self.object_corp = tb_corporations.get_row(self.corporation_id, service_module)
        if self.alliance_id is not None:
            self.object_alliance = tb_alliances.get_row(self.alliance_id, service_module)

    def get_api(self, configuration):
        return swagger_client.CharacterApi(swagger_client.ApiClient(configuration))

    def get_response(self, api, token):
        return api.get_characters_character_id_with_http_info(self.character_id, datasource='tranquility',
                                                              user_agent="my_test_agent",
                                                              if_none_match=str(self.api_ETag))

    def new_pull_needed(self):
        try:
            assert self.name is not None
            return False
        except AssertionError:
            return True

    @classmethod
    def primary_key_row(cls):
        return cls.character_id
