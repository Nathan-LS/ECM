from database.tables.base_api_one_one import *
from database.tables import *


class Constellations(Base, api_one_to_one):
    __tablename__ = 'constellations'

    constellation_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, default=None, nullable=True)
    region_id = Column(Integer, ForeignKey("regions.region_id"), nullable=False)

    api_ETag = Column(String, default=None, nullable=True)
    api_Expires = Column(DateTime, default=None, nullable=True)
    api_Last_Modified = Column(DateTime, default=None, nullable=True)

    object_region = relationship("Regions", uselist=False, back_populates="object_constellations")
    object_systems = relationship("Systems", cascade="delete", back_populates="object_constellation")

    def __init__(self, eve_id: int):
        self.constellation_id = eve_id

    def api_populate_fk_objects(self, service_module):
        if self.region_id is not None:
            self.object_region = tb_regions.get_row(self.region_id, service_module)

    def get_api(self, configuration):
        return swagger_client.UniverseApi(swagger_client.ApiClient(configuration))

    def get_response(self, api, token):
        return api.get_universe_constellations_constellation_id_with_http_info(constellation_id=self.constellation_id,
                                                                               datasource='tranquility',
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
        return cls.constellation_id
