from selenium.webdriver.support.select import Select
from Model.address import Address
import re

class AddressHelper:

    def __init__(self, app):
        self.app = app

    def add_address(self, address):
        wd = self.app.wd
        self.open_home_page()
        self.open_add_address()
        self.fill_address_form(address)
        self.submit_add_address()
        self.return_home_page()
        self.contact_cache = None

    def open_home_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/addressbook/") and len(wd.find_elements_by_name("Send e-Mail")) > 0):
            wd.get("http://localhost:8080/addressbook/")

    def fill_address_form(self, Address):
        wd = self.app.wd
        self.type_address_value("firstname", Address.firstname)
        self.type_address_value("lastname", Address.lastname)
        self.type_address_value("address", Address.address)
        self.type_address_value("email", Address.email)
        self.type_address_value("mobile", Address.mobile)

    def type_address_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def return_home_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/addressbook/") and len(wd.find_elements_by_name("Send e-Mail")) > 0):
            wd.find_element_by_link_text("home").click()

    def submit_add_address(self):
        wd = self.app.wd
        wd.find_element_by_xpath("(//input[@name='submit'])[2]").click()


    def del_address_by_index(self, index):
        wd = self.app.wd
        #select first address
        self.select_some_address(index)
        #select delete button
        wd.find_element_by_xpath("//div[@class='left'][2]/input").click()
        #click ok on allert
        wd.switch_to_alert().accept()
        self.contact_cache = None

    def del_address_by_id(self, id):
        wd = self.app.wd
        #select first address
        self.select_address_by_id(id)
        #select delete button
        wd.find_element_by_xpath("//input[@value='Delete']").click()
        #wd.switch_to_alert().accept()
        self.contact_cache = None

    def select_first_address(self):
        wd = self.app.wd
        self.select_some_address(0)

    def select_some_address(self, index):
        wd = self.app.wd
        wd.find_elements_by_name("selected[]")[index].click()


    def editfirst_address(self):
        wd = self.app.wd
        self.editsome_address(0)

    def editsome_address(self, index):
        wd = self.app.wd
        self.open_home_page()
        row = wd.find_elements_by_name("entry")[index]
        cells = row.find_elements_by_tag_name("td")[7]
        cells.find_element_by_tag_name("a").click()

    def select_address_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_css_selector("a[href='edit.php?id=%s']" % id).click()

    def edit_address(self, index, new_address_data):
        wd = self.app.wd
        self.return_home_page()
        self.editsome_address(index)
        #Change text
        self.fill_address_form(new_address_data)
        #Update
        wd.find_element_by_name("update").click()
        self.contact_cache = None

    def edit_address_by_id(self, id, new_address_data):
        wd = self.app.wd
        self.return_home_page()
        self.select_address_by_id(id)
        #Change text
        self.fill_address_form(new_address_data)
        #Update
        wd.find_element_by_name("update").click()
        self.return_home_page()
        self.contact_cache = None


    def open_add_address(self):
        wd = self.app.wd
        wd.find_element_by_link_text("add new").click()

    def count_address(self):
        wd = self.app.wd
        self.open_home_page()
        return len(wd.find_elements_by_name("selected[]"))


    contact_cache = None

    def get_address_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            self.open_home_page()
            self.contact_cache = []
            for element in wd.find_elements_by_css_selector("tr[name='entry']"):
                id = element.find_element_by_name("selected[]").get_attribute("value")
                cells = element.find_elements_by_tag_name("td")
                l_name = cells[1].text
                f_name = cells[2].text
                address = cells[3].text
                all_phones = cells[5].text
                all_emails = cells[4].text
                self.contact_cache.append(Address(id=id, firstname=f_name, lastname=l_name, all_phones_from_home_page=all_phones, all_emails_from_home_page=all_emails, address=address))
        return list(self.contact_cache)

    def open_address_view_by_index(self, index):
        wd = self.app.wd
        self.open_home_page()
        row = wd.find_elements_by_name("entry")[index]
        cells = row.find_elements_by_tag_name("td")[6]
        cells.find_element_by_tag_name("a").click()

    def get_address_info_from_editpage(self, index):
        wd = self.app.wd
        self.editsome_address(index)
        firstname = wd.find_element_by_name("firstname").get_attribute("value")
        lastname = wd.find_element_by_name("lastname").get_attribute("value")
        id = wd.find_element_by_name("id").get_attribute("value")
        home = wd.find_element_by_name("home").get_attribute("value")
        work = wd.find_element_by_name("work").get_attribute("value")
        mobile = wd.find_element_by_name("mobile").get_attribute("value")
        phone2 = wd.find_element_by_name("phone2").get_attribute("value")
        address = wd.find_element_by_name("address").get_attribute("value")
        email = wd.find_element_by_name("email").get_attribute("value")
        email2 = wd.find_element_by_name("email2").get_attribute("value")
        email3 = wd.find_element_by_name("email3").get_attribute("value")
        return Address(id=id, firstname=firstname, lastname=lastname, home=home, mobile=mobile,
                       work=work, phone2=phone2, address=address, email=email, email2=email2, email3=email3)


    def get_address_from_view_page(self, index):
        wd = self.app.wd
        self.open_address_view_by_index(index)
        text = wd.find_element_by_id("content").text
        home = re.search("H: (.*)", text).group(1)
        mobile = re.search("M: (.*)", text).group(1)
        work = re.search("W: (.*)", text).group(1)
        phone2 = re.search("P: (.*)", text).group(1)
        return Address(home=home, work=work, mobile=mobile, phone2=phone2)

    def get_emails_from_view_page(self, index):
        wd = self.app.wd
        self.open_address_view_by_index(index)
        for element in wd.find_elements_by_css_selector("div#content"):
            cells = element.find_elements_by_tag_name("a")
            email = cells[0].text
            email2 = cells[1].text
            email3 = cells[2].text
            return Address(email=email, email2=email2, email3=email3)


