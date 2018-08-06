from database.tables.base_api_one_one import *
from database.tables import *


class Corporations(Base, api_one_to_one):
    __tablename__ = 'corporations'

    corporation_id = Column(Integer, primary_key=True, nullable=False)
    alliance_id = Column(Integer, ForeignKey("alliances.alliance_id"), nullable=True)
    ceo_id = Column(Integer, default=None, nullable=True)  # fk
    creator_id = Column(Integer, default=None, nullable=True)
    date_founded = Column(DateTime, default=None, nullable=True)
    description = Column(String, default=None, nullable=True)
    faction_id = Column(Integer, default=None, nullable=True)
    home_station_id = Column(Integer, default=None, nullable=True)
    member_count = Column(Integer, default=0, nullable=True)
    name = Column(String, default=None, nullable=False)
    shares = Column(Integer, default=0, nullable=True)
    tax_rate = Column(Float, default=0, nullable=False)
    ticker = Column(String, default=None, nullable=True)
    url = Column(String, default=None, nullable=True)

    api_ETag = Column(String, default=None, nullable=True)
    api_Expires = Column(DateTime, default=None, nullable=True)
    api_Last_Modified = Column(DateTime, default=None, nullable=True)

    object_characters = relationship("Characters", back_populates="object_corp")
    object_alliance = relationship("Alliances", uselist=False, back_populates="object_corps")

    def __init__(self, corp_id):
        self.corporation_id = corp_id

    def api_populate_fk_objects(self, service_module):
        if self.alliance_id is not None:
            self.object_alliance = tb_alliances.get_row(self.alliance_id, service_module)

    def get_api(self, configuration):
        return swagger_client.CorporationApi(swagger_client.ApiClient(configuration))

    def get_response(self, api, token):
        return api.get_corporations_corporation_id_with_http_info(self.corporation_id, datasource='tranquility',
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
        return cls.corporation_id
