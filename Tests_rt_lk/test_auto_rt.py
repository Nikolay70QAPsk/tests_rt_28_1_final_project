import pytest

from pages.auth_page import AuthPage
from pages.registration_page import RegPage


# Тест-кейс TK_RT-001
# Корректное отображение "Стандартной страницы авторизации"
def test_start_page_is_correct(web_browser):
    page = AuthPage(web_browser)
    phone_tab_class = page.phone_tab.get_attribute("class")
    assert phone_tab_class == "rt-tab rt-tab--small rt-tab--active"
    assert page.phone.is_clickable()
    assert page.password.is_clickable()
    assert page.btn_login.is_clickable()
    assert page.registration_link.is_clickable()
    assert page.auth_title.get_text() == "Авторизация"
    assert page.logo_lk.get_text() == "Личный кабинет"


# Тест-кейс TK_RT-002 (FB-1)
# Проверка элементов в левом и правом блоке страницы
@pytest.mark.xfail(reason="Расположение элементов на странице не соответсвует ожидаемым требованиям")
def test_location_of_page_blocks(web_browser):
    page = AuthPage(web_browser)
    assert page.auth_form.find(timeout=1)
    assert page.lk_form.find(timeout=1)


# Тест-кейс TK_RT-003 (FB-2)
# Проверка названия таб выбора "Номер"
@pytest.mark.xfail(reason="Таб выбора 'Номер' не соответсвует ожидаемым требованиям")
def test_phone_tab(web_browser):
    page = AuthPage(web_browser)
    assert page.phone_tab.get_text() == "Номер"


# Тест-кейс TK_RT-004 (FB-3)
# Проверка название кнопки "Продолжить" в форме "Регистрация"
@pytest.mark.xfail(reason="Кнопка должна иметь текст 'Продолжить'")
def test_registration_page_and_continue_button(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    assert reg_page.name_field_text.get_text() == "Имя"
    assert reg_page.last_name_field_text.get_text() == "Фамилия"
    assert reg_page.region_field_text.get_text() == "Регион"
    assert reg_page.email_or_mobile_phone_field_text.get_text() == "E-mail или мобильный телефон"
    assert reg_page.password_field_text.get_text() == "Пароль"
    assert reg_page.password_confirmation_field_text.get_text() == "Подтверждение пароля"
    assert reg_page.continue_button.get_text() == "Продолжить"


# Тест-кейс TK_RT-005
# Регистрация пользователя с пустым полем "Имя", появления текста с подсказкой об ошибке
def test_registration_page_with_empty_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys('')
    reg_page.last_name_field.send_keys("Ветров")
    reg_page.email_or_mobile_phone_field.send_keys("vetrov@yandex.ru")
    reg_page.password_field.send_keys("Qwert1234")
    reg_page.password_confirmation_field.send_keys("Qwert1234")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс ТК_RT-006
# Регистрация пользователя с некорректным значением в поле "Имя"(< 2 символов), появление текста с подскаской об ошибке
def test_registration_with_an_incorrect_value_in_the_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys('Н')
    reg_page.last_name_field.send_keys("Ветров")
    reg_page.email_or_mobile_phone_field.send_keys("vetrov@yandex.ru")
    reg_page.password_field.send_keys("Qwert1234")
    reg_page.password_confirmation_field.send_keys("Qwert1234")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс ТК_RT-007
# Регистрация пользователя с некорректным значением в поле "Фамилия"(>30 символов), появление текста с подсказкой об ошибке
def test_registration_with_an_incorrect_value_in_the_last_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Николай")
    reg_page.last_name_field.send_keys("ЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛПЛЛЛЛЛРЛЛЛЛЛЛЛЛД")
    reg_page.email_or_mobile_phone_field.send_keys("vetrov@yandex.ru")
    reg_page.password_field.send_keys("Qwert1234")
    reg_page.password_confirmation_field.send_keys("Qwert1234")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_last_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс ТК_RT-008
# Регистрация пользователя с уже зарегистрированным номером, отображается оповещающая форма
def test_registration_of_an_already_registered_user(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Н")
    reg_page.last_name_field.send_keys("ННИРПППЛЛЛЛЛЛЛЛЛЛЛ")
    reg_page.email_or_mobile_phone_field.send_keys("+79532742244")
    reg_page.password_field.send_keys("wTuyr34565672")
    reg_page.password_confirmation_field.send_keys("wTuyr34565672")
    reg_page.continue_button.click()
    assert reg_page.notification_form.is_visible


# Тест-кейс ТК_RT-009 (FB-4)
# Проверка кнопки "х" - закрыть всплывающее окно оповещения
@pytest.mark.xfail(reason="Должна быть кнопка закрыть 'х'")
def test_notification_form(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Н")
    reg_page.last_name_field.send_keys("ЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛ")
    reg_page.email_or_mobile_phone_field.send_keys("+79532742244")
    reg_page.password_field.send_keys("www12345Q")
    reg_page.password_confirmation_field.send_keys("www12345Q")
    reg_page.continue_button.click()
    assert reg_page.login_button.get_text() == 'Войти'
    assert reg_page.recover_password_button.get_text() == 'Восстановить пароль'
    assert reg_page.close_button.get_text() == 'x'


# Тест-кейс ТК_RT-010
# Некорректный пароль при регистрации пользователя (< 8 символов), появления текста с подсказкой об ошибке
def test_incorrect_password_during_registration(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Николай")
    reg_page.last_name_field.send_keys("Ветров")
    reg_page.email_or_mobile_phone_field.send_keys("vetrov@yandex.ru")
    reg_page.password_field.send_keys("www")
    reg_page.password_confirmation_field.send_keys("www")
    reg_page.continue_button.click()
    assert reg_page.error_message_password.get_text() == "Длина пароля должна быть не менее 8 символов"


# Тест-кейс ТК_RT-011
# Вход по неправильному паролю в форме "Авторизация" уже зарегистрированного пользователя, надпись "Забыл пароль"
# перекрашивается в оранжнвый цвет
def test_authorization_of_a_user_with_an_invalid_password(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('+79532742244')
    page.password.send_keys("www")
    page.btn_login.click()
    assert page.message_invalid_username_or_password.get_text() == "Неверный логин или пароль"
    assert "rt-link--orange" in page.the_element_forgot_the_password.get_attribute('class')


# Тест-кейс ТК_RT-012
# Регистрация пользователя в форме "Регистрации" в поле ввода "Фамилия" вместо кириллицы недопустимые символы
def test_instead_of_cyrillic_invalid_characters(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Николай")
    reg_page.last_name_field.send_keys("%?*%№!><")
    reg_page.email_or_mobile_phone_field.send_keys("vetrov@yandex.ru")
    reg_page.password_field.send_keys("Qwert1234")
    reg_page.password_confirmation_field.send_keys("Qwert1234")
    reg_page.continue_button.click()
    assert reg_page.message_must_be_filled_in_cyrillic.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс ТК_RT-013
# Поле ввода "Пароль" и поле ввода "Подтверждение пароля"  в форме "Регистрация" не совпадают
def test_password_and_password_confirmation_do_not_match(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Николай")
    reg_page.last_name_field.send_keys("Ветров")
    reg_page.email_or_mobile_phone_field.send_keys("vetrov@yandex.ru")
    reg_page.password_field.send_keys("Qwert1234")
    reg_page.password_confirmation_field.send_keys("1234Mbdfr")
    reg_page.continue_button.click()
    assert reg_page.message_passwords_dont_match.get_text() == "Пароли не совпадают"


# Тест-кейс TK_RT-014
# Не валидный email в поле ввода "Email или мобильный телефон"
def test_invalid_email_or_mobile_phone(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Николай")
    reg_page.last_name_field.send_keys("Маркелов")
    reg_page.email_or_mobile_phone_field.send_keys("11111111111")
    reg_page.password_field.send_keys("Qwert1234")
    reg_page.password_confirmation_field.send_keys("Qwert1234")
    reg_page.continue_button.click()
    assert reg_page.message_enter_the_phone_in_the_format.get_text() == "Введите телефон в формате +7ХХХХХХХХХХ или" \
                                                                        " +375XXXXXXXXX, или email в формате example@email.ru"


# Тест-кейс ТК_RT-015
# Тестирование аутентификации зарегистрированного пользователя
def test_authorisation_valid(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('+79999999999')
    page.password.send_keys("Qwert1234")
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
           and '&client_id=account_b2c#/' in page.get_current_url()


# Тест-кейс ТК_RT-016
# Проверка перехода по ссылке авторизации пользователя через сайт vk
def test_auth_vk(web_browser):
    page = AuthPage(web_browser)
    page.auth_btn_vk.click()

    assert 'oauth.vk.com' == page.get_current_url()


# Тест-кейс ТК_RT-017
# Проверка перехода по ссылке авторизации пользователя через сайт ok
def test_auth_ok(web_browser):
    page = AuthPage(web_browser)
    page.auth_btn_ok.click()

    assert 'connect.ok.ru' in page.get_current_url()


# Тест-кейс ТК_RT-018
# Проверка перехода по ссылке авторизации пользователя через сайт мой мир.mail.ru
def test_auth_mail(web_browser):
    page = AuthPage(web_browser)
    page.auth_btn_mail.click()

    assert 'connect.mail.ru' in page.get_current_url()


# Тест-кейс ТК_RT-019
# Проверка перехода по ссылке авторизации пользователя через сайт google
def test_auth_google(web_browser):
    page = AuthPage(web_browser)
    page.auth_btn_google.click()

    assert 'accounts.google.com' in page.get_current_url()


# Тест-кейс ТК_RT-020
# Проверка перехода по ссылке авторизации пользователя через сайт yandex
def test_auth_yandex(web_browser):
    page = AuthPage(web_browser)
    page.auth_btn_ya.click()

    assert 'passport.yandex.ru' in page.get_current_url()

