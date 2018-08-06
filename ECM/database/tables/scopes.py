from database.tables.base_api_one_one import *
from database.tables import *


class Scopes(Base, api_one_one_no_auto_pull):
    __tablename__ = 'scopes'

    scope = Column(String, primary_key=True)
    read_write = Column(String)
    used = Column(Boolean, default=False, nullable=False)

    tokens_with_scope = relationship("Token_scopes", uselist=True, cascade="delete", back_populates="object_scope")

    def __init__(self, type: str, scope_name: str, used: bool = False):
        self.scope = scope_name
        self.read_write = type
        self.used = used

    def __repr__(self):
        return (str(self.__dict__))

    @staticmethod
    def make_default_scopes(service_module: service):
        db: Session = service_module.get_session()
        db.merge(Scopes('write', 'esi-calendar.respond_calendar_events.v1'))
        db.merge(Scopes('read', 'esi-calendar.read_calendar_events.v1'))
        db.merge(Scopes('read', 'esi-location.read_location.v1', used=True))
        db.merge(Scopes('read', 'esi-location.read_ship_type.v1', used=True))
        db.merge(Scopes('write', 'esi-mail.organize_mail.v1'))
        db.merge(Scopes('read', 'esi-mail.read_mail.v1'))
        db.merge(Scopes('write', 'esi-mail.send_mail.v1'))
        db.merge(Scopes('read', 'esi-skills.read_skills.v1', used=True))
        db.merge(Scopes('read', 'esi-skills.read_skillqueue.v1', used=True))
        db.merge(Scopes('read', 'esi-wallet.read_character_wallet.v1', used=True))
        db.merge(Scopes('read', 'esi-wallet.read_corporation_wallet.v1'))
        db.merge(Scopes('read', 'esi-search.search_structures.v1'))
        db.merge(Scopes('read', 'esi-characters.read_contacts.v1'))
        db.merge(Scopes('read', 'esi-universe.read_structures.v1'))
        db.merge(Scopes('read', 'esi-bookmarks.read_character_bookmarks.v1'))
        db.merge(Scopes('read', 'esi-killmails.read_killmails.v1', used=True))
        db.merge(Scopes('read', 'esi-corporations.read_corporation_membership.v1'))
        db.merge(Scopes('read', 'esi-assets.read_assets.v1', used=True))
        db.merge(Scopes('write', 'esi-planets.manage_planets.v1'))
        db.merge(Scopes('read', 'esi-fleets.read_fleet.v1'))
        db.merge(Scopes('write', 'esi-fleets.write_fleet.v1'))
        db.merge(Scopes('write', 'esi-ui.open_window.v1'))
        db.merge(Scopes('write', 'esi-ui.write_waypoint.v1'))
        db.merge(Scopes('write', 'esi-characters.write_contacts.v1'))
        db.merge(Scopes('read', 'esi-fittings.read_fittings.v1'))
        db.merge(Scopes('write', 'esi-fittings.write_fittings.v1'))
        db.merge(Scopes('read', 'esi-markets.structure_markets.v1'))
        db.merge(Scopes('read', 'esi-corporations.read_structures.v1'))
        db.merge(Scopes('write', 'esi-corporations.write_structures.v1'))
        db.merge(Scopes('read', 'esi-characters.read_loyalty.v1'))
        db.merge(Scopes('read', 'esi-characters.read_opportunities.v1'))
        db.merge(Scopes('read', 'esi-characters.read_chat_channels.v1'))
        db.merge(Scopes('read', 'esi-characters.read_medals.v1'))
        db.merge(Scopes('read', 'esi-characters.read_standings.v1'))
        db.merge(Scopes('read', 'esi-characters.read_agents_research.v1'))
        db.merge(Scopes('read', 'esi-industry.read_character_jobs.v1'))
        db.merge(Scopes('read', 'esi-markets.read_character_orders.v1'))
        db.merge(Scopes('read', 'esi-characters.read_blueprints.v1'))
        db.merge(Scopes('read', 'esi-characters.read_corporation_roles.v1'))
        db.merge(Scopes('read', 'esi-location.read_online.v1'))
        db.merge(Scopes('read', 'esi-contracts.read_character_contracts.v1'))
        db.merge(Scopes('read', 'esi-clones.read_implants.v1'))
        db.merge(Scopes('read', 'esi-characters.read_fatigue.v1', used=True))
        db.merge(Scopes('read', 'esi-killmails.read_corporation_killmails.v1'))
        db.merge(Scopes('read', 'esi-corporations.track_members.v1'))
        db.merge(Scopes('read', 'esi-wallet.read_corporation_wallets.v1'))
        db.merge(Scopes('read', 'esi-characters.read_notifications.v1'))
        db.merge(Scopes('read', 'esi-corporations.read_divisions.v1'))
        db.merge(Scopes('read', 'esi-corporations.read_contacts.v1'))
        db.merge(Scopes('read', 'esi-assets.read_corporation_assets.v1'))
        db.merge(Scopes('read', 'esi-corporations.read_blueprints.v1'))
        db.merge(Scopes('read', 'esi-bookmarks.read_corporation_bookmarks.v1'))
        db.merge(Scopes('read', 'esi-contracts.read_corporation_contracts.v1'))
        db.merge(Scopes('read', 'esi-corporations.read_standings.v1'))
        db.merge(Scopes('read', 'esi-corporations.read_starbases.v1'))
        db.merge(Scopes('read', 'esi-industry.read_corporation_jobs.v1'))
        db.merge(Scopes('read', 'esi-markets.read_corporation_orders.v1'))
        db.merge(Scopes('read', 'esi-corporations.read_container_logs.v1'))
        db.merge(Scopes('read', 'esi-industry.read_character_mining.v1'))
        db.merge(Scopes('read', 'esi-industry.read_corporation_mining.v1'))
        db.merge(Scopes('read', 'esi-planets.read_customs_offices.v1'))
        db.merge(Scopes('read', 'esi-corporations.read_facilities.v1'))
        db.merge(Scopes('read', 'esi-corporations.read_medals.v1'))
        db.merge(Scopes('read', 'esi-characters.read_titles.v1'))
        db.merge(Scopes('read', 'esi-alliances.read_contacts.v1'))
        db.merge(Scopes('read', 'esi-characters.read_fw_stats.v1'))
        db.merge(Scopes('read', 'esi-corporations.read_fw_stats.v1'))
        db.merge(Scopes('read', 'esi-corporations.read_outposts.v1'))
        db.merge(Scopes('read', 'esi-characterstats.read.v1', used=True))
        db.commit()
        service_module.close_session()

    @classmethod
    def primary_key_row(cls):
        return cls.scope
