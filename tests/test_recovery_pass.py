import allure
import pytest

from data.urls import Urls
from data.user_data import PersonData


class TestRecoveryPassword:

    @allure.title('Проверка на переход по клику на Восстановить пароль на странице логина')
    def test_click_password_reset_button(self, base_page, main_page, recovery_password_page):
        main_page.click_on_account()
        recovery_password_page.click_password_reset_link()
        current_url = base_page.get_current_url()
        assert current_url == Urls.url_restore

    @allure.title('Проверка на ввод почты и переход после клика по кнопке "Восстановить"')
    def test_enter_email_and_click_reset(self, base_page, main_page, recovery_password_page):
        base_page.open_link(Urls.url_restore)
        recovery_password_page.set_email_for_reset_password(PersonData.user_login)
        recovery_password_page.click_reset_button()
        recovery_password_page.find_save_button()
        current_url = base_page.get_current_url()
        assert current_url == Urls.url_reset

    @allure.title('Проверка что клик по кнопке показать/скрыть пароль делает поле активным')
    def test_make_field_active(self, base_page, main_page, recovery_password_page):
        base_page.open_link(Urls.url_restore)
        recovery_password_page.set_email_for_reset_password(PersonData.user_login)
        recovery_password_page.click_reset_button()
        recovery_password_page.find_save_button()
        recovery_password_page.click_on_show_password_button()
        assert recovery_password_page.find_input_active()
