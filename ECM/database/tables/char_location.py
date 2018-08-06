from database.tables.base_api_one_one import *
from database.tables import *


class Char_location(Base, api_one_one_no_auto_pull):
    __tablename__ = 'char_location'

    character_id = Column(Integer, ForeignKey(tb_tokens.for_character), primary_key=True, nullable=False)
    solar_system_id = Column(Integer, ForeignKey(tb_systems.system_id), default=None, nullable=True)
    station_id = Column(Integer, default=None, nullable=True)
    structure_id = Column(Integer, default=None, nullable=True)

    api_ETag = Column(String, default=None, nullable=True)
    api_Expires = Column(DateTime, default=None, nullable=True)
    api_Last_Modified = Column(DateTime, default=None, nullable=True)

    object_system = relationship("Systems", uselist=False, back_populates="object_pilots_in_system")
    object_token = relationship("Tokens", uselist=False, back_populates="object_char_location")

    def __init__(self, pilot_id: int):
        self.character_id = pilot_id

    def api_populate_fk_objects(self, service_module):
        if self.solar_system_id:
            self.object_system = tb_systems.get_row(self.solar_system_id, service_module)

    def get_api(self, configuration):
        return swagger_client.LocationApi(swagger_client.ApiClient(configuration))

    def get_response(self, api, token):
        return api.get_characters_character_id_location_with_http_info(self.character_id, datasource='tranquility',
                                                                       token=token,
                                                                       user_agent="my_test_agent",
                                                                       if_none_match=str(self.api_ETag))

    @classmethod
    def primary_key_row(cls):
        return cls.character_id
