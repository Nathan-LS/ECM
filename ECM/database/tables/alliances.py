from database.tables.base_api_one_one import *
from database.tables import *


class Alliances(Base, api_one_to_one):
    __tablename__ = 'alliances'

    alliance_id = Column(Integer, primary_key=True, nullable=False)
    creator_corporation_id = Column(Integer, default=None, nullable=True)
    creator_id = Column(Integer, default=None, nullable=True)
    date_founded = Column(DateTime, default=None, nullable=True)
    executor_corporation_id = Column(Integer, default=None, nullable=True)
    faction_id = Column(Integer, default=None, nullable=True)
    name = Column(String, default="", nullable=False)
    ticker = Column(String, default="", nullable=False)

    api_ETag = Column(String, default=None, nullable=True)
    api_Expires = Column(DateTime, default=None, nullable=True)
    api_Last_Modified = Column(DateTime, default=None, nullable=True)

    object_corps = relationship("Corporations", back_populates="object_alliance")
    object_characters = relationship("Characters", back_populates="object_alliance")

    def __init__(self, eve_id):
        self.alliance_id = eve_id

    def get_api(self, configuration):
        return swagger_client.AllianceApi(swagger_client.ApiClient(configuration))

    def get_response(self, api, token):
        return api.get_alliances_alliance_id_with_http_info(self.alliance_id, datasource='tranquility',
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
        return cls.alliance_id
