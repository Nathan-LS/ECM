from PyQt5.QtCore import QObject
import service.service_module
from sqlalchemy import *
import swagger_client
from sqlalchemy.orm import scoped_session, Session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from misc.dynamic_values import *
from database.tables import *
from service.logger import logger
from database.load_db import load_db
from service.settings import settings
from service.web_listener import web_listener
from service.pilot import Pilot
from service.character_manager import character_manager
from service.image_serve import image_serve
from service.scheduler import Scheduler_service


class Service_Module(QObject):
    def __init__(self):
        super(Service_Module, self).__init__()
        load_database = load_db()
        self.sc_session: scoped_session = load_database.get_scoped_session()
        tb_scopes.make_default_scopes(service_module=self)
        self.logger = logger(service_module=self)
        self.settings = settings(service_module=self)
        self.callback_listener: web_listener = web_listener(service_module=self)
        self.callback_listener.start()
        self.images = image_serve(service_module=self)
        self.scheduler = Scheduler_service()
        self.characters = character_manager(service_module=self)
        assert isinstance(self.sc_session, scoped_session)
        assert isinstance(self.logger, logger)
        assert isinstance(self.settings, settings)
        assert isinstance(self.callback_listener, web_listener)
        assert isinstance(self.images, image_serve)
        assert isinstance(self.scheduler, Scheduler_service)

    def get_session(self) -> Session:
        """

        :rtype: Session
        """
        session_object: Session = self.sc_session()
        assert isinstance(session_object, Session)
        return session_object

    def close_session(self):
        self.sc_session.remove()
