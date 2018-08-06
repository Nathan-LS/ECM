from database.tables.base_api_one_one import *
from database.tables import *


class Regions(Base, api_one_to_one):
    __tablename__ = 'regions'

    region_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, default=None, nullable=True)
    description = Column(String, default=None, nullable=True)

    api_ETag = Column(String, default=None, nullable=True)
    api_Expires = Column(DateTime, default=None, nullable=True)
    api_Last_Modified = Column(DateTime, default=None, nullable=True)

    object_constellations = relationship("Constellations", cascade="delete", back_populates="object_region")

    def __init__(self, eve_id: int):
        self.region_id = eve_id

    def get_api(self, configuration):
        return swagger_client.UniverseApi(swagger_client.ApiClient(configuration))

    def get_response(self, api, token):
        return api.get_universe_regions_region_id_with_http_info(region_id=self.region_id, datasource='tranquility',
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
        return cls.region_id
