from database.tables.base_api_one_one import *
from database.tables import *


class Systems(Base, api_one_to_one):
    __tablename__ = 'systems'

    system_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, default=None, nullable=True)
    constellation_id = Column(Integer, ForeignKey("constellations.constellation_id"), nullable=False)
    security_class = Column(String, default=None, nullable=True)
    security_status = Column(Float, default=0.0, nullable=True)
    star_id = Column(Integer, default=None, nullable=True)

    api_ETag = Column(String, default=None, nullable=True)
    api_Expires = Column(DateTime, default=None, nullable=True)
    api_Last_Modified = Column(DateTime, default=None, nullable=True)

    object_constellation = relationship("Constellations", uselist=False, back_populates="object_systems")
    object_pilots_in_system = relationship("Char_location", back_populates="object_system")

    def __init__(self, eve_id: int):
        self.system_id = eve_id

    def api_populate_fk_objects(self, service_module):
        if self.constellation_id is not None:
            self.object_constellation = tb_constellations.get_row(self.constellation_id, service_module)

    def get_api(self, configuration):
        return swagger_client.UniverseApi(swagger_client.ApiClient(configuration))

    def get_response(self, api, token):
        return api.get_universe_systems_system_id_with_http_info(system_id=self.system_id, datasource='tranquility',
                                                                 user_agent="my_test_agent",
                                                                 if_none_match=str(self.api_ETag))

    def new_pull_needed(self):
        try:
            assert self.name is not None
            assert self.object_constellation is not None
            return False
        except AssertionError:
            return True

    @classmethod
    def primary_key_row(cls):
        return cls.system_id
