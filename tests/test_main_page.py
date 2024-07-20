import time

import allure
import pytest

from data.urls import Urls


class TestMainPage:

    @allure.title('По кнопке «Лента заказов» совершается переход на страницу заказов')
    @allure.description('При нажатии в header кнопки "Лента заказов" перенаправляет на страницу со всеми заказами')
    def test_redirection_to_order_list(self, main_page):
        main_page.click_orders_list_button()
        current_url = main_page.get_current_url()
        assert current_url == Urls.url_feed

    @allure.title('При нажатии в header кнопки "Конструктор" совершается переход на старницу сбора бургера')
    @allure.description('При нажатии в header кнопки "Конструктор"  происходит редирект на страницу со всеми заказами')
    def test_go_to_constructor(self, main_page):
        main_page.click_orders_list_button()
        main_page.click_constructor_button()
        current_url = main_page.get_current_url()
        assert current_url == Urls.url_main

    @allure.title('При нажатии на ингридиент всплывает окно с информаций')
    @allure.description('При нажатии на игридиент всплывает модальное окно с информацией об ингридиенте')
    def test_popup_of_ingredient(self, main_page):
        main_page.click_on_ingredient()
        actually_text = main_page.check_show_window_with_details()
        assert actually_text == "Детали ингредиента"

    @allure.title('При нажатии в модальном окне с информацией об ингридиенте крестика , окно закрывается')
    @allure.description('Нажимает на крестик в правом верхнем углу окна и проверяем, что всплывающее окно закрылось')
    def test_close_ingredient_details_window(self, main_page):
        main_page.click_on_ingredient()
        main_page.click_cross_button()
        main_page.invisibility_ingredient_details()
        assert main_page.check_displayed_ingredient_details() == False

    @allure.title('При добавлении ингридиента в заказ, счетчик увеличивается')
    @allure.description('Проверяем что после добавления ингридиента счетчик ингридента сменился')
    def test_ingredient_counter(self, main_page):
        prev_counter_value = main_page.get_count_value()
        main_page.add_filling_to_order()
        print(main_page.get_count_value())
        actual_value = main_page.get_count_value()
        assert actual_value > prev_counter_value

    @allure.title('Проверка возможности оформления заказ авторизованным пользователем')
    @allure.description('Нажимаем кнопку «Оформить заказ» и проверяем, что заказ оформлен и появился идентификатор заказа')
    def test_successful_order(self, main_page, login):
        main_page.add_filling_to_order()
        main_page.click_order_button()
        actually_text = main_page.check_show_window_with_order_id()
        assert actually_text == "идентификатор заказа" and main_page.check_displayed_order_status_text() == True
