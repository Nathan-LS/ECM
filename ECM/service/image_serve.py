from PyQt5.QtGui import QPixmap
from service.service_module import *
from service.service_module import *
import requests
import os


class image_serve(QObject):
    def __init__(self, service_module):
        super(image_serve, self).__init__()
        self.service = service_module
        assert isinstance(self.service, service.service_module.Service_Module)
        self.host = "https://image.eveonline.com"
        self.cache_dir = "media"
        self.icon_exception = "media/static/icons/icon_exception.png"
        self.icon_404 = "media/static/icons/icon_404.png"

    def __file_exists(self, local_image_path) -> bool:
        return os.path.isfile(local_image_path)

    def __download_image(self, local_image_path, ccp_image_path):
        os.makedirs(os.path.dirname(local_image_path), exist_ok=True)
        try:
            response = requests.get("https://image.eveonline.com/{}".format(ccp_image_path), allow_redirects=True)
            if response.status_code == 200:
                with open(local_image_path, 'wb') as file:
                    file.write(response.content)
                return local_image_path
            elif response.status_code == 404:
                return self.icon_404
        except Exception as ex:
            if self.__file_exists(local_image_path):
                return local_image_path
            else:
                return self.icon_exception

    def __get_path(self, category, id, width, extension, redownload: bool = False):
        image_path = "{ty}/{i_id}_{res}.{ex}".format(ty=category, i_id=str(id), res=str(width), ex=extension)
        abs_image_path = "{}/{}".format(self.cache_dir, image_path)
        if self.__file_exists(abs_image_path) and not redownload:
            return abs_image_path
        else:
            return self.__download_image(abs_image_path, image_path)

    def __make_pixmap(self, path) -> QPixmap:
        return QPixmap(path)

    def get_pilot(self, pilot_id: int, pull_new=False) -> QPixmap:
        return self.__make_pixmap(self.__get_path("Character", pilot_id, 512, "jpg", pull_new))

    def get_corp(self, corp_id: int, pull_new: bool = False) -> QPixmap:
        return self.__make_pixmap(self.__get_path("Corporation", corp_id, 256, "png", pull_new))

    def get_alliance(self, alliance_id: int, pull_new: bool = False) -> QPixmap:
        return self.__make_pixmap(self.__get_path("Alliance", alliance_id, 128, "png", pull_new))

    def get_inventory_type(self, typeID: int, pull_new: bool = False) -> QPixmap:
        return self.__make_pixmap(self.__get_path("Type", typeID, 64, "png", pull_new))

    def get_ship_render(self, typeID: int, pull_new: bool = False) -> QPixmap:
        return self.__make_pixmap(self.__get_path("Render", typeID, 512, "png", pull_new))
