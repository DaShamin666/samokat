import allure
import pytest
from config.environments import Environment, environments

@allure.feature("Тесты для проверки функциональности кнопок аккордеона на главной странице.")
class TestAccordionButtons:
    
    @pytest.mark.smoke
    @allure.title("Проверка кликов по всем кнопкам FAQ и отображения соответствующих текстов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_click_all_accordion_buttons_and_check_text_visibility(self, app, click_accordion_buttons):
        """
        Тест проверяет клики по всем кнопкам FAQ и отображение текстов.

        """
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step("Выполнить клики по всем кнопкам FAQ и проверить отображение текстов"):
            click_accordion_buttons()
    
    @pytest.mark.regression
    @allure.title("Проверка отдельных кнопок FAQ")
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

        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step(f"Кликнуть по кнопке '{button_name}' и проверить отображение"):
            app.home_page.click_accordion_button_by_key(button_key, text_key)
