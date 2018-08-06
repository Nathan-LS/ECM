from service.service_module import *
from database.base import Base


class load_db(object):
    sc_session: scoped_session

    def __init__(self, file="Database.db"):
        self.engine = create_engine('sqlite:///{}'.format(file),
                                    connect_args={'check_same_thread': False, 'timeout': 3000}, echo=False)
        self.create_tables()
        Session = sessionmaker(bind=self.engine)
        self.sc_session = scoped_session(Session)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def get_scoped_session(self):
        return self.sc_session
