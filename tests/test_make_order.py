import time

import allure
import pytest

from data.urls import Urls
from web_locators import OrdersPageLocators


class TestCreateOrder:
    @allure.title('Проверка появления всплывающего окна с деталями при клике на заказ')
    @allure.description('Кликаем на заказ и проверяем, что появилось всплывающее окно с деталями')
    def test_get_order_popup(self, main_page, test_create_order_page):
        main_page.click_orders_list_button()
        test_create_order_page.click_order()
        assert test_create_order_page.check_order_structure() == True

    @allure.title('При создании заказа этот заказа отображается как и в История заказов в ЛК профиля, так и в "Ленте заказов"')
    @allure.description('Соpдаем заказа и проверяем есть ли он в ЛК в Истории заказов и есть ли этот же заказ в "Ленте заказов"')
    def test_find_order_in_list(self, main_page, user_profile_page, test_create_order_page, login):
        main_page.add_filling_to_order()
        main_page.click_order_button()
        main_page.check_show_window_with_order_id()
        order_number = main_page.get_with_order_id()
        main_page.click_close_modal_order()
        main_page.click_on_account()
        user_profile_page.click_order_history_button()
        is_order_id_found_at_history = test_create_order_page.is_order_id_found_at_history(order_number)
        main_page.click_orders_list_button()
        is_order_id_found_at_feed = test_create_order_page.is_order_id_found_at_feed(order_number)
        assert is_order_id_found_at_history and is_order_id_found_at_feed, "Заказы в истории и в ленте не совпадают"

    @allure.title('При создании заказа, происходит увеличения значения счетчиков заказов "Выполнено за все время"/"Выполнено за сегодня"')
    @allure.description('Сверяем счетчик заказов "Выполнено за все время" / "Выполнено за сегодня" до создания заказа и после создания заказа '
                        'Счетчик должен увеличиться')
    @pytest.mark.parametrize('counter', [OrdersPageLocators.TOTAL_ORDER_COUNT, OrdersPageLocators.DAILY_ORDER_COUNT])
    def test_today_orders_counter(self, main_page, test_create_order_page, login, counter):
        main_page.click_orders_list_button()
        prev_counter_value = test_create_order_page.get_total_order_count_daily(counter)
        main_page.click_constructor_button()
        main_page.add_filling_to_order()
        main_page.click_order_button()
        main_page.click_close_modal_order()
        main_page.click_orders_list_button()
        current_counter_value = test_create_order_page.get_total_order_count_daily(counter)
        assert current_counter_value > prev_counter_value, "Заказ не создался, counter не сработал"

    @allure.title('Проверка отображения номера заказа в разделе "В работе')
    @allure.description('Получаем номер нового заказа, и проверяем, что номер заказа появился в разделе "В работе"')
    def test_new_order_appears_in_work_list(self, main_page, test_create_order_page, login):
        main_page.add_filling_to_order()
        main_page.click_order_button()
        order_number = main_page.get_with_order_id()
        main_page.click_close_modal_order()
        main_page.click_orders_list_button()
        order_number_refactor = test_create_order_page.get_user_order(order_number)
        order_in_progress = test_create_order_page.get_user_order_in_progress()
        assert order_number_refactor == order_in_progress
