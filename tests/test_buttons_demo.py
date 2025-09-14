import allure
import pytest
from playwright.sync_api import expect
from config.environments import Environment, environments

@allure.feature("Демонстрационные тесты для проверки работы обеих кнопок заказа.")
class TestButtonsDemo:

    @pytest.mark.smoke
    @allure.title("Демонстрация работы верхней и нижней кнопок заказа")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_both_buttons_navigation_demo(self, app, order_button_type, click_order_button):
        """Демонстрационный тест навигации через обе кнопки."""
        button_names = {"top": "верхняя", "bottom": "нижняя"}
        button_name = button_names[order_button_type]
        
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step(f"Кликнуть по {button_name} кнопке заказа"):
            click_order_button(order_button_type)
        
        with allure.step("Проверить, что отображается форма заказа"):
            expect(app.order_page.name_input).to_be_visible()
            expect(app.order_page.surname_input).to_be_visible()
            
        with allure.step("Заполнить минимальные данные"):
            app.order_page.fill_minimal_demo_data(button_name)
            
        with allure.step("Проверить, что форма заполнена"):
            expect(app.order_page.name_input).to_have_value(f"Тест_{button_name}")
            expect(app.order_page.phone_input).to_have_value("+79991234567")

    @pytest.mark.regression
    @allure.title("Сравнение кнопок - одинаковый результат")
    @allure.severity(allure.severity_level.NORMAL)
    def test_buttons_lead_to_same_form(self, app):
        """Тест сравнения результата клика по разным кнопкам."""
        env_config = environments[Environment.DEV]
        
        with allure.step("Тест верхней кнопки"):
            app.home_page.open(env_config.url)
            app.home_page.navigate_to_order_form_via_top_button()
            expect(app.order_page.name_input).to_be_visible()
            page_title_1 = app.page.title()
            
        with allure.step("Тест нижней кнопки"):
            app.home_page.open(env_config.url)
            app.home_page.navigate_to_order_form_via_bottom_button()
            expect(app.order_page.name_input).to_be_visible()
            page_title_2 = app.page.title()
            
        with allure.step("Проверить, что результат одинаковый"):
            expect(app.page).to_have_title(page_title_1)
            assert page_title_1 == page_title_2  # Временно оставляем assert для проверки логики

    @pytest.mark.smoke
    @allure.title("Проверка текста на кнопках")
    @allure.severity(allure.severity_level.MINOR)
    def test_buttons_text(self, app):
        """Тест проверки текста на кнопках."""
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step("Проверить текст верхней кнопки"):
            expect(app.home_page.order_button_top).to_have_text("Заказать")
            
        with allure.step("Прокрутить к нижней кнопке"):
            app.home_page.order_button_bottom.scroll_into_view_if_needed()
            
        with allure.step("Проверить текст нижней кнопки"):
            expect(app.home_page.order_button_bottom).to_have_text("Заказать")
