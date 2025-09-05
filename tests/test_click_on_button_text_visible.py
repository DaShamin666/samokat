import allure
import pytest
from config.environments import Environment, environments


class TestAccordionButtons:
    """Тесты для проверки функциональности кнопок аккордеона на главной странице."""
    
    @pytest.mark.smoke
    @allure.title("Проверка кликов по всем кнопкам FAQ и отображения соответствующих текстов")
    @allure.description("""
    Тест проверяет:
    1. Возможность кликнуть по каждой кнопке аккордеона в секции FAQ
    2. Отображение соответствующего текста после клика
    3. Видимость кнопки после клика
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_click_all_accordion_buttons_and_check_text_visibility(self, app, click_accordion_buttons):
        """
        Тест проверяет клики по всем кнопкам FAQ и отображение текстов.
        
        Args:
            app: Фикстура приложения для навигации
            click_accordion_buttons: Фикстура для выполнения кликов по кнопкам аккордеона
        """
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step("Выполнить клики по всем кнопкам FAQ и проверить отображение текстов"):
            click_accordion_buttons()
    
    @pytest.mark.regression
    @allure.title("Проверка отдельных кнопок FAQ")
    @allure.description("Тест для проверки отдельных кнопок FAQ с параметризацией")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("button_key,text_key,button_name", [
        ("how_much_button", "how_much", "Сколько это стоит? И как оплатить?"),
        ("several_scooters", "several_scooters", "Хочу заказать несколько самокатов"),
        ("time_arenda", "time_arenda", "Как рассчитывается время аренды?"),
        ("zakaz_today", "zakaz_today", "Можно ли заказать самокат прямо на сегодня?"),
        ("prodlit_and_vernut", "prodlit_and_vernut", "Можно ли продлить заказ или вернуть самокат раньше?"),
        ("zarydka_on_samokat", "zarydka_on_samokat", "Вы привозите зарядку вместе с самокатом?"),
        ("otmena_zakaza", "otmena_zakaza", "Можно ли отменить заказ?"),
        ("zamkadish", "zamkadish", "Я живу за МКАДом, привезёте?"),
    ])
    def test_individual_accordion_button(self, app, button_key, text_key, button_name):
        """
        Тест проверяет отдельные кнопки FAQ.
        
        Args:
            app: Фикстура приложения
            button_key: Ключ кнопки в объекте home_page
            text_key: Ключ текста в словаре texts
            button_name: Название кнопки для отчета
        """
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step(f"Кликнуть по кнопке '{button_name}'"):
            button = getattr(app.home_page, button_key)
            button.click()
        
        with allure.step(f"Проверить отображение кнопки '{button_name}'"):
            from playwright.sync_api import expect
            expect(button).to_be_visible()
        
        with allure.step(f"Проверить отображение текста для '{button_name}'"):
            from playwright.sync_api import expect
            expect(app.home_page.texts[text_key]).to_be_visible()
