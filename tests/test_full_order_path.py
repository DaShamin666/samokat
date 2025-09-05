import allure
import pytest
from playwright.sync_api import expect
from config.environments import Environment, environments


class TestFullOrderPath:
    """Тесты полного пути заказа для обеих кнопок заказа."""
    
    @pytest.mark.regression
    @allure.title("Полный путь заказа через верхнюю и нижнюю кнопки")
    @allure.description("Проверяет полный путь заказа от клика по кнопке до завершения заказа для обеих кнопок")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_complete_order_path_both_buttons(self, test_user, order_button_type, complete_order_from_button):
        """
        Параметризованный тест полного пути заказа для обеих кнопок.
        Тест запустится 2 раза: для верхней и нижней кнопки.
        """
        button_names = {"top": "верхней", "bottom": "нижней"}
        button_name = button_names[order_button_type]
        
        with allure.step(f"Выполнить полный заказ через {button_name} кнопку"):
            complete_order_from_button(
                button_type=order_button_type,
                user_data=test_user,
                metro_station="Сокольники",
                delivery_date="15.12.2024",
                rental_period="сутки",
                comment=f"Заказ через {button_name} кнопку для {test_user.name}"
            )
        
        # Проверка успешного завершения будет внутри фикстуры

    @pytest.mark.regression
    @allure.title("Тестирование разных станций метро для обеих кнопок")
    @allure.description("Проверяет выбор разных станций метро при заказе через обе кнопки")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("metro_station", [
        "Сокольники",
        "Красносельская", 
        "Комсомольская",
        "Курская"
    ])
    def test_metro_stations_both_buttons(self, test_user, order_button_type, 
                                       complete_order_from_button, metro_station):
        """Тест выбора разных станций метро для обеих кнопок."""
        button_names = {"top": "верхней", "bottom": "нижней"}
        button_name = button_names[order_button_type]
        
        with allure.step(f"Заказ через {button_name} кнопку со станцией {metro_station}"):
            complete_order_from_button(
                button_type=order_button_type,
                user_data=test_user,
                metro_station=metro_station,
                delivery_date="20.12.2024",
                rental_period="сутки",
                comment=f"Станция {metro_station} через {button_name} кнопку"
            )

    @pytest.mark.regression
    @allure.title("Тестирование разных периодов аренды для обеих кнопок")
    @allure.description("Проверяет выбор разных периодов аренды при заказе через обе кнопки")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("rental_period", [
        "сутки",
        "двое суток",
        "трое суток",
        "четверо суток"
    ])
    def test_rental_periods_both_buttons(self, test_user, order_button_type, 
                                       complete_order_from_button, rental_period):
        """Тест выбора разных периодов аренды для обеих кнопок."""
        button_names = {"top": "верхней", "bottom": "нижней"}
        button_name = button_names[order_button_type]
        
        with allure.step(f"Заказ через {button_name} кнопку на {rental_period}"):
            complete_order_from_button(
                button_type=order_button_type,
                user_data=test_user,
                metro_station="Сокольники",
                delivery_date="25.12.2024",
                rental_period=rental_period,
                comment=f"Период {rental_period} через {button_name} кнопку"
            )

    @pytest.mark.regression
    @allure.title("Сравнительный тест - одинаковые данные через разные кнопки")
    @allure.description("Проверяет, что заказ с одинаковыми данными работает через обе кнопки")
    @allure.severity(allure.severity_level.NORMAL)
    def test_same_data_different_buttons(self, test_user, complete_order_from_button):
        """Тест с одинаковыми данными через разные кнопки."""
        
        # Общие данные для обоих заказов
        order_data = {
            "user_data": test_user,
            "metro_station": "Комсомольская",
            "delivery_date": "30.12.2024",
            "rental_period": "двое суток",
        }
        
        with allure.step("Первый заказ через верхнюю кнопку"):
            complete_order_from_button(
                button_type="top",
                comment="Первый заказ - верхняя кнопка",
                **order_data
            )
        
        with allure.step("Второй заказ через нижнюю кнопку"):
            complete_order_from_button(
                button_type="bottom",
                comment="Второй заказ - нижняя кнопка",
                **order_data
            )


class TestOrderButtonsNavigation:
    """Тесты навигации и отображения кнопок заказа."""
    
    @pytest.mark.smoke
    @allure.title("Проверка видимости и доступности обеих кнопок заказа")
    @allure.description("Проверяет, что обе кнопки заказа видимы и кликабельны на главной странице")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_both_order_buttons_visibility(self, app):
        """Тест видимости обеих кнопок заказа."""
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step("Проверить видимость верхней кнопки заказа"):
            expect(app.order_page.one_button_order).to_be_visible()
            expect(app.order_page.one_button_order).to_be_enabled()
        
        with allure.step("Прокрутить к нижней кнопке"):
            app.order_page.second_button_order.scroll_into_view_if_needed()
        
        with allure.step("Проверить видимость нижней кнопки заказа"):
            expect(app.order_page.second_button_order).to_be_visible()
            expect(app.order_page.second_button_order).to_be_enabled()

    @pytest.mark.smoke
    @allure.title("Проверка перехода к форме заказа через обе кнопки")
    @allure.description("Проверяет, что обе кнопки корректно ведут к форме заказа")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navigation_to_order_form(self, app, order_button_type, click_order_button):
        """Параметризованный тест перехода к форме заказа."""
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
            expect(app.order_page.adres_input).to_be_visible()

    @pytest.mark.regression
    @allure.title("Проверка заполнения первого шага через обе кнопки")
    @allure.description("Проверяет заполнение первого шага формы заказа, запущенной через обе кнопки")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_first_step_completion_both_buttons(self, app, test_user, order_button_type, 
                                              click_order_button, fill_order_form_step1):
        """Тест заполнения первого шага через обе кнопки."""
        button_names = {"top": "верхняя", "bottom": "нижняя"}
        button_name = button_names[order_button_type]
        
        with allure.step("Открыть главную страницу"):
            env_config = environments[Environment.DEV]
            app.home_page.open(env_config.url)
        
        with allure.step(f"Перейти к форме заказа через {button_name} кнопку"):
            click_order_button(order_button_type)
        
        with allure.step(f"Заполнить первый шаг формы (пользователь: {test_user.name})"):
            fill_order_form_step1(test_user, metro_station="Курская")
        
        with allure.step("Проверить переход ко второму шагу"):
            expect(app.order_page.date_input).to_be_visible()
            expect(app.order_page.rental_period_dropdown).to_be_visible()


class TestOrderPathEdgeCases:
    """Тесты граничных случаев для пути заказа."""
    
    @pytest.mark.regression
    @allure.title("Множественные заказы через разные кнопки")
    @allure.description("Проверяет создание нескольких заказов подряд через разные кнопки")
    @allure.severity(allure.severity_level.NORMAL)
    def test_multiple_orders_alternating_buttons(self, complete_order_from_button):
        """Тест создания нескольких заказов через разные кнопки по очереди."""
        from config.environments import UserCredentials
        
        buttons = ["top", "bottom", "top"]  # Чередуем кнопки
        
        for i, button_type in enumerate(buttons):
            user = UserCredentials.generate_fake()
            button_name = "верхняя" if button_type == "top" else "нижняя"
            
            with allure.step(f"Заказ #{i+1} через {button_name} кнопку"):
                complete_order_from_button(
                    button_type=button_type,
                    user_data=user,
                    metro_station="Сокольники",
                    delivery_date=f"{15+i}.12.2024",
                    rental_period="сутки",
                    comment=f"Заказ #{i+1} через {button_name} кнопку"
                )

    @pytest.mark.regression
    @allure.title("Проверка с разными типами пользователей через обе кнопки")
    @allure.description("Проверяет заказ с предопределенными пользователями через обе кнопки")
    @allure.severity(allure.severity_level.NORMAL)
    def test_predefined_users_both_buttons(self, any_user, order_button_type, complete_order_from_button):
        """Тест с предопределенными пользователями через обе кнопки."""
        button_names = {"top": "верхняя", "bottom": "нижняя"}
        button_name = button_names[order_button_type]
        
        with allure.step(f"Заказ пользователя {any_user.email} через {button_name} кнопку"):
            complete_order_from_button(
                button_type=order_button_type,
                user_data=any_user,
                metro_station="Красносельская",
                delivery_date="31.12.2024",
                rental_period="двое суток",
                comment=f"Предопределенный пользователь через {button_name} кнопку"
            )
