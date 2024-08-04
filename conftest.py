import allure
import pytest
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.firefox import webdriver
from selenium import webdriver
from data.urls import Urls
from web_pages.auth_user_page import AuthUserPage
from web_pages.base_page import BasePage
from web_pages.main_page import MainPage
from web_pages.recovery_password_page import PasswordRecoveryPage
from web_pages.test_create_order_page import CreateOrderPage
from web_pages.user_profile_page import UserProfilePage




@allure.step('Открытие браузер')
@pytest.fixture(params=['chrome', 'firefox'])
def driver_do(request):
    if request.param == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get(Urls.url_main)


    elif request.param == 'firefox':
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--headless')
        driver = webdriver.Firefox(options=firefox_options)
        driver.set_window_size(1920, 1080)
        driver.get(Urls.url_main)
    yield driver
    driver.quit()


@pytest.fixture(scope='function')
def auth_user_page(driver_do):
    return AuthUserPage(driver_do)

@pytest.fixture(scope='function')
def recovery_password_page(driver_do):
    return PasswordRecoveryPage(driver_do)


@pytest.fixture(scope='function')
def base_page(driver_do):
    return BasePage(driver_do)


@pytest.fixture(scope='function')
def main_page(driver_do):
    return MainPage(driver_do)


@pytest.fixture(scope='function')
def test_create_order_page(driver_do):
    return CreateOrderPage(driver_do)


@pytest.fixture(scope='function')
def user_profile_page(driver_do):
    return UserProfilePage(driver_do)


@pytest.fixture(scope='function')
def login(auth_user_page):
#    """ Войти в аккаунт """
    auth_user_page.login()