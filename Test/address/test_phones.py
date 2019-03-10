import re
#обратная проверка (склейка)
def test_phones_on_homepage(app):
    contact_from_home_page = app.Contacts.get_address_list()[0]
    contact_from_edit_page = app.Contacts.get_address_info_from_editpage(0)
    assert contact_from_home_page.all_phones_from_homepage == merge_phone_on_home_page(contact_from_edit_page)

#прямая проверка (вырезка)
def test_phones_on_view_page(app):
    contact_from_view_page = app.Contacts.get_address_from_view_page(0)
    contact_from_edit_page = app.Contacts.get_address_info_from_editpage(0)
    assert contact_from_view_page.homephone == contact_from_edit_page.homephone
    assert contact_from_view_page.mobilephone == contact_from_edit_page.mobilephone
    assert contact_from_view_page.workphone == contact_from_edit_page.workphone
    assert contact_from_view_page.secondphone == contact_from_edit_page.secondphone


def clear(s):
    return re.sub("[, ], -, +, ()", "", s)


def merge_phone_on_home_page(contact):
    return "\n".join(filter(lambda x: x != "",
                            map (lambda x: clear(x),
                                 filter(lambda x: x is not None,
                                    [contact.homephone, contact.mobilephone, contact.workphone, contact.secondphone]))))