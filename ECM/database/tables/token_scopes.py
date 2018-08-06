from database.tables.base_api_one_one import *
from database.tables import *


class Token_scopes(Base, api_one_one_no_auto_pull):
    __tablename__ = 'token_scopes'

    pilot_id = Column(Integer, ForeignKey("tokens.for_character"), primary_key=True, nullable=False)
    scope = Column(String, ForeignKey("scopes.scope"), primary_key=True, nullable=False)

    object_token = relationship("Tokens", uselist=False, back_populates="object_token_scopes")
    object_scope = relationship("Scopes", uselist=False, back_populates="tokens_with_scope")

    def __init__(self, ob_token, ob_scope):
        self.object_token = ob_token
        self.object_scope = ob_scope

    @classmethod
    def get_row(cls, id, service_module: service):
        return service_module.get_session().query(cls).filter(cls.pilot_id == id).all()
