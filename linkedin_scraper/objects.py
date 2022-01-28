from dataclasses import dataclass
from typing import Optional

from selenium.webdriver import Chrome

from . import constants as c


@dataclass
class Contact:
    name: str = None
    occupation: str = None
    url: str = None


@dataclass
class Institution:
    institution_name: str = None
    website: str = None
    industry: str = None
    type: str = None
    headquarters: str = None
    company_size: int = None
    founded: int = None


@dataclass
class Experience(Institution):
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    description: Optional[str] = None
    position_title: Optional[str] = None
    duration: Optional[str] = None
    location: Optional[str] = None
    institution_name: Optional[str] = None


@dataclass
class Education(Institution):
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    description: Optional[str] = None
    degree: Optional[str] = None


@dataclass
class Interest(Institution):
    title = None


@dataclass
class Accomplishment(Institution):
    category = None
    title = None


@dataclass
class Scraper:
    driver: Chrome = None

    def is_signed_in(self):
        try:
            self.driver.find_element_by_id(c.VERIFY_LOGIN_ID)
            return True
        except:
            pass
        return False

    def __find_element_by_class_name__(self, class_name):
        try:
            self.driver.find_element_by_class_name(class_name)
            return True
        except:
            pass
        return False

    def __find_element_by_xpath__(self, tag_name):
        try:
            self.driver.find_element_by_xpath(tag_name)
            return True
        except:
            pass
        return False

    def __find_enabled_element_by_xpath__(self, tag_name):
        try:
            elem = self.driver.find_element_by_xpath(tag_name)
            return elem.is_enabled()
        except:
            pass
        return False

    @classmethod
    def __find_first_available_element__(cls, *args):
        for elem in args:
            if elem:
                return elem[0]
