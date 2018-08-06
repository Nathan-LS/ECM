from database.tables.base_api_one_one import *
from database.tables import *


class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, default=1)
    status_bar_clock_online_count = Column(Integer, default=40, nullable=False)  # time between updates
    User_Agent = Column(String, default="my-test-agent", nullable=False)
    API_Host = Column(String, default="https://esi.tech.ccp.is", nullable=False)
    client_id = Column(String, default=None, nullable=True)
    secret_key = Column(String, default=None, nullable=True)

    def __repr__(self):
        return (str(self.__dict__))
