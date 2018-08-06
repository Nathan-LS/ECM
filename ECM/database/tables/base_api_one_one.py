from database.base import Base
from service.service_module import *
import swagger_client
from swagger_client.rest import ApiException
from swagger_client import Configuration
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship, backref
from sqlalchemy.inspection import inspect


class api_one_to_one(object):
    def api_populate(self, token: str = None):
        try:
            r = self.get_response(self.get_api(self.get_cofiguration(token)), token)
            local_variables = vars(self)
            for key, value in r[0].to_dict().items():
                try:
                    local_variables[key] = value
                except Exception as ex:
                    print(ex)
            try:
                local_variables["api_ETag"] = r[2].get("Etag")
                self.api_Expires = datetime.datetime.strptime(r[2].get("Expires"),
                                                              '%a, %d %b %Y %H:%M:%S %Z')  # Mon, 11 Jun 2018 23:34:52 GMT
                # local_variables["api_Expires"] = datetime.datetime.strptime(r[2].get("Expires"),'%a, %d %b %Y %H:%M:%S %Z') #Mon, 11 Jun 2018 23:34:52 GMT
                local_variables["api_Last_Modified"] = datetime.datetime.strptime(r[2].get("Last-Modified"),
                                                                                  '%a, %d %b %Y %H:%M:%S %Z')
            except Exception as ex:
                print(ex)
            return 200
        except ApiException as ex:
            try:
                return ex.status
            except:
                return 0  # todo fix other
        except Exception as ex:
            return 0

    def api_populate_fk_objects(self, service_module):
        pass

    def api_static_populate(self):  # no token needed
        raise NotImplementedError

    def get_cofiguration(self, token):
        configuration = swagger_client.Configuration()
        configuration.access_token = token
        return configuration

    def get_api(self, configuration):
        raise NotImplementedError
        # return swagger_client.SkillsApi(swagger_client.ApiClient(configuration))

    def get_response(self, api, token):
        raise NotImplementedError
        # return api.get_characters_character_id_attributes(self.character_id,datasource='tranquility',token=token,user_agent="my_test_agent")

    def new_pull_needed(self):
        return False

    @classmethod
    def primary_key_row(cls):
        raise NotImplementedError

    @classmethod
    def get_row(cls, id, service_module: service):
        db: Session = service_module.get_session()
        try:
            __row = db.query(cls).filter(cls.primary_key_row() == id).one()
            if __row.new_pull_needed():
                __row.api_populate()
            __row.api_populate_fk_objects(service_module)
            return __row
        except NoResultFound:
            __row = cls(id)
            __row.api_populate()
            __row.api_populate_fk_objects(service_module)
            return __row


class api_one_one_no_auto_pull(api_one_to_one):
    @classmethod
    def get_row(cls, id, service_module: service):
        db: Session = service_module.get_session()
        try:
            __row = db.query(cls).filter(cls.primary_key_row() == id).one()
            return __row
        except NoResultFound:
            __row = cls(id)
            return __row
