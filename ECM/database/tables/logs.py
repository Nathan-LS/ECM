from database.tables.base_api_one_one import *
from database.tables import *


class log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime)
    type = Column(String)
    message = Column(String)

    def __init__(self, time: datetime, type: str, message: str):
        self.time = time
        self.type = type
        self.message = message

    def __repr__(self):
        return (str(self.__dict__))
