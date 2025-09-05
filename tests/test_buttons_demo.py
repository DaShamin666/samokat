import allure
import pytest
from playwright.sync_api import expect
from config.environments import Environment, environments


class TestButtonsDemo:
    """Демонстрационные тесты для проверки работы обеих кнопок заказа."""
    
    @pytest.mark.smoke
    @allure.title("Демонстрация работы верхней и нижней кнопок заказа")
    @allure.description("Простой тест, показывающий что обе кнопки работают и ведут к форме заказа")
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
            app.order_page.name_input.fill(f"Тест_{button_name}")
            app.order_page.surname_input.fill("Пользователь")
            app.order_page.adres_input.fill("ул. Тестовая 1")
            
        with allure.step("Выбрать станцию метро"):
            app.order_page.metro_input.click()
            # Ждем появления опций и выбираем первую
            app.order_page.metro_choice.first.click(timeout=5000)
            
        with allure.step("Ввести телефон"):
            app.order_page.phone_input.fill("+79991234567")
            
        # На этом останавливаемся, не переходим ко второму шагу
        with allure.step("Проверить, что форма заполнена"):
            expect(app.order_page.name_input).to_have_value(f"Тест_{button_name}")
            expect(app.order_page.phone_input).to_have_value("+79991234567")

    @pytest.mark.regression
    @allure.title("Сравнение кнопок - одинаковый результат")
    @allure.description("Проверяет, что обе кнопки ведут к одинаковой форме заказа")
    @allure.severity(allure.severity_level.NORMAL)  
    def test_buttons_lead_to_same_form(self, app):
        """Тест сравнения результата клика по разным кнопкам."""
        env_config = environments[Environment.DEV]
        
        # Тест верхней кнопки
        with allure.step("Тест верхней кнопки"):
            app.home_page.open(env_config.url)
            app.order_page.one_button_order.click()
            expect(app.order_page.name_input).to_be_visible()
            page_title_1 = app.page.title()
            
        # Тест нижней кнопки  
        with allure.step("Тест нижней кнопки"):
            app.home_page.open(env_config.url)
            app.order_page.second_button_order.scroll_into_view_if_needed()
            app.order_page.second_button_order.click()
            expect(app.order_page.name_input).to_be_visible()
            page_title_2 = app.page.title()
            
        with allure.step("Проверить, что результат одинаковый"):
            assert page_title_1 == page_title_2, f"Заголовки страниц отличаются: '{page_title_1}' != '{page_title_2}'"

    @pytest.mark.smoke
    @allure.title("Проверка текста на кнопках")
    @allure.description("Проверяет, что на обеих кнопках корректный текст 'Заказать'")
    @allure.severity(allure.severity_level.MINOR)
    def test_buttons_text(self, app):
        """Тест проверки текста на кнопках."""
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step("Проверить текст верхней кнопки"):
            expect(app.order_page.one_button_order).to_have_text("Заказать")
            
        with allure.step("Прокрутить к нижней кнопке"):
            app.order_page.second_button_order.scroll_into_view_if_needed()
            
        with allure.step("Проверить текст нижней кнопки"):
            expect(app.order_page.second_button_order).to_have_text("Заказать")
