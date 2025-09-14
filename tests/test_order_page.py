import allure
import pytest
from playwright.sync_api import expect
from config.environments import Environment, environments, UserCredentials

@allure.feature("Тесты для страницы заказа самоката и валидации формы")
class TestOrderPage:
    """Тесты для страницы заказа самоката и валидации формы."""
    
    @pytest.mark.smoke
    @allure.title("Переход к форме заказа через кнопку 'Заказать' (верхняя)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_order_button_top_navigation(self, app):
        """Тест перехода к форме заказа через верхнюю кнопку."""
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step("Кликнуть по верхней кнопке 'Заказать'"):
            app.home_page.navigate_to_order_form_via_top_button()
        
        with allure.step("Проверить, что отображается форма заказа"):
            expect(app.order_page.name_input).to_be_visible()
    
    @pytest.mark.smoke
    @allure.title("Переход к форме заказа через кнопку 'Заказать' (нижняя)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_order_button_bottom_navigation(self, app):
        """Тест перехода к форме заказа через нижнюю кнопку."""
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step("Кликнуть по нижней кнопке 'Заказать'"):
            app.home_page.navigate_to_order_form_via_bottom_button()
        
        with allure.step("Проверить, что отображается форма заказа"):
            expect(app.order_page.name_input).to_be_visible()

    @pytest.mark.regression
    @allure.title("Заполнение первого шага формы заказа с рандомными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_fill_order_form_step1_random_user(self, app, test_user, fill_order_form_step1):
        """Тест заполнения первого шага формы заказа с рандомными данными."""
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step("Перейти к форме заказа"):
            app.home_page.navigate_to_order_form_via_top_button()
        
        with allure.step(f"Заполнить форму данными пользователя: {test_user.name} {test_user.surname}"):
            fill_order_form_step1(test_user)
        
        with allure.step("Проверить переход ко второму шагу"):
            expect(app.order_page.date_input).to_be_visible()

    @allure.title("Заполнение первого шага формы заказа с предопределенными данными")
    @allure.severity(allure.severity_level.NORMAL)
    def test_fill_order_form_step1_predefined_user(self, app, predefined_user, fill_order_form_step1):
        """Тест заполнения первого шага формы заказа с предопределенными данными."""
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step("Перейти к форме заказа"):
            app.home_page.navigate_to_order_form_via_top_button()
        
        with allure.step(f"Заполнить форму данными user_order: {predefined_user.email}"):
            fill_order_form_step1(predefined_user)
        
        with allure.step("Проверить переход ко второму шагу"):
            expect(app.order_page.date_input).to_be_visible()

    @pytest.mark.regression
    @allure.title("Полный цикл оформления заказа")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_complete_order_flow(self, app, test_user, complete_order_flow):
        """Тест полного цикла оформления заказа."""
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step("Перейти к форме заказа"):
            app.home_page.navigate_to_order_form_via_top_button()
        
        with allure.step(f"Оформить заказ для пользователя: {test_user.name} {test_user.surname}"):
            complete_order_flow(
                user_data=test_user,
                metro_station="Сокольники",
                delivery_date="15.12.2024",
                rental_period="сутки",
                comment=f"Заказ для {test_user.name}"
            )
        
        with allure.step("Проверить успешное оформление заказа"):
            expect(app.order_page.order_success_header).to_be_visible()

    @allure.title("Тестирование с разными типами пользователей")
    @allure.severity(allure.severity_level.NORMAL)
    def test_order_with_different_user_types(self, app, any_user, fill_order_form_step1):
        """Параметризованный тест с разными типами пользователей."""
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step("Перейти к форме заказа"):
            app.home_page.navigate_to_order_form_via_top_button()
        
        with allure.step(f"Заполнить форму данными пользователя: {any_user.email}"):
            fill_order_form_step1(any_user)
        
        with allure.step("Проверить переход ко второму шагу"):
            expect(app.order_page.date_input).to_be_visible()

    @allure.title("Тестирование выбора разных станций метро")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("metro_station", [
        "Сокольники",
        "Красносельская", 
        "Комсомольская",
        "Курская"
    ])
    def test_metro_station_selection(self, app, test_user, fill_order_form_step1, metro_station):
        """Тест выбора разных станций метро."""
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step("Перейти к форме заказа"):
            app.home_page.navigate_to_order_form_via_top_button()
        
        with allure.step(f"Заполнить форму с выбором станции метро: {metro_station}"):
            fill_order_form_step1(test_user, metro_station)
        
        with allure.step("Проверить переход ко второму шагу"):
            expect(app.order_page.date_input).to_be_visible()

    @allure.title("Тестирование разных периодов аренды")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("rental_period", [
        "сутки",
        "двое суток",
        "трое суток",
        "четверо суток",
        "пятеро суток",
        "шестеро суток",
        "семеро суток"
    ])
    def test_rental_period_selection(self, app, test_user, fill_order_form_step1, 
                                   fill_order_form_step2, rental_period):
        """Тест выбора разных периодов аренды."""
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step("Перейти к форме заказа"):
            app.home_page.navigate_to_order_form_via_top_button()
        
        with allure.step("Заполнить первый шаг формы"):
            fill_order_form_step1(test_user)
        
        with allure.step(f"Заполнить второй шаг с периодом аренды: {rental_period}"):
            fill_order_form_step2(
                delivery_date="20.12.2024",
                rental_period=rental_period,
                comment=f"Тест периода: {rental_period}"
            )
        
        with allure.step("Проверить успешное оформление заказа"):
            expect(app.order_page.order_success_header).to_be_visible()

    @allure.title("Проверка обязательных полей первого шага")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_required_fields_validation_step1(self, app):
        """Тест валидации обязательных полей первого шага."""
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step("Перейти к форме заказа"):
            app.home_page.navigate_to_order_form_via_top_button()
        
        with allure.step("Попытаться отправить пустую форму"):
            app.order_page.click_next_button()
        
        with allure.step("Проверить, что форма не отправилась (остались на первом шаге)"):
            expect(app.order_page.name_input).to_be_visible()

    @allure.title("Создание нескольких заказов подряд")
    @allure.severity(allure.severity_level.NORMAL)
    def test_multiple_orders_creation(self, app, complete_order_flow):
        """Тест создания нескольких заказов подряд."""
        env_config = environments[Environment.DEV]
        
        for i in range(3):
            user = UserCredentials.generate_fake()
            
            with allure.step(f"Создание заказа #{i+1} для {user.name} {user.surname}"):
                with allure.step("Открыть главную страницу"):
                    app.home_page.open(env_config.url)
                
                with allure.step("Перейти к форме заказа"):
                    app.home_page.navigate_to_order_form_via_top_button()
                
                with allure.step(f"Оформить заказ #{i+1}"):
                    complete_order_flow(
                        user_data=user,
                        comment=f"Заказ номер {i+1}"
                    )
                
                with allure.step(f"Проверить успешное оформление заказа #{i+1}"):
                    expect(app.order_page.order_success_header).to_be_visible()
