from selenium.webdriver.firefox.webdriver import WebDriver
from Fixture.session import SessionHelper
from Fixture.group import GroupHelper
from Fixture.Contacts import AddressHelper


class Application:


    def __init__(self):
        self.wd = WebDriver()
        self.wd.implicitly_wait(60)
        self.session = SessionHelper(self)
        self.Group = GroupHelper(self)
        self.Contacts = AddressHelper(self)

    def open_home_page(self):
        wd = self.wd
        wd.get("http://localhost/addressbook/")

    def destroy(self):
        self.wd.quit()