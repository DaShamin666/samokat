import allure
import pytest
from config.environments import Environment, environments

@allure.feature("Демонстрационные тесты для проверки работы обеих кнопок заказа.")
class TestButtonsDemo:

    @allure.title("Демонстрация работы верхней и нижней кнопок заказа")
    @pytest.mark.smoke
    @allure.severity(allure.severity_level.CRITICAL)
    def test_both_buttons_navigation_demo(self, app,open_main_page, order_button_type, click_order_button):
        button_names = {"top": "верхняя", "bottom": "нижняя"}
        button_name = button_names[order_button_type]

        
        with allure.step(f"Кликнуть по {button_name} кнопке заказа"):
            click_order_button(order_button_type)
        
        with allure.step("Проверить, что отображается форма заказа"):
            app.order_page.verify_order_form_displayed()
            
        with allure.step("Заполнить минимальные данные"):
            app.order_page.fill_minimal_demo_data(button_name)

    @allure.title("Сравнение кнопок - одинаковый результат")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    def test_buttons_lead_to_same_form(self, app):
        """Тест сравнения результата клика по разным кнопкам."""
        env_config = environments[Environment.DEV]
        
        with allure.step("Тест верхней кнопки"):
            app.home_page.open(env_config.url)
            app.home_page.navigate_to_order_form_via_top_button()
            page_title_1 = app.page.title()
            
        with allure.step("Тест нижней кнопки"):
            app.home_page.open(env_config.url)
            app.home_page.navigate_to_order_form_via_bottom_button()
            page_title_2 = app.page.title()
            
        with allure.step("Проверить, что результат одинаковый"):
            assert page_title_1 == page_title_2

    @allure.title("Проверка текста на кнопках")
    @pytest.mark.smoke
    @allure.severity(allure.severity_level.MINOR)
    def test_buttons_text(self, app,open_main_page):

        with allure.step("Проверить текст на кнопках заказа"):
            app.home_page.verify_order_buttons_text()
