import allure
import pytest
from config.environments import Environment, environments
from config.environments import UserCredentials


@allure.feature("Тесты полного пути заказа для обеих кнопок заказа и граничные случаи.")
class TestFullOrderPath:

    @allure.title("Полный путь заказа через верхнюю и нижнюю кнопки")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.BLOCKER)
    def test_complete_order_path_both_buttons(self, test_user, order_button_type, complete_order_from_button):

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


    @allure.title("Тестирование разных станций метро для обеих кнопок")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("metro_station", [
        "Сокольники",
        "Красносельская", 
        "Комсомольская",
        "Курская"
    ])
    def test_metro_stations_both_buttons(self, test_user, order_button_type, 
                                       complete_order_from_button, metro_station):
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

    @allure.title("Тестирование разных периодов аренды для обеих кнопок")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("rental_period", [
        "сутки",
        "двое суток",
        "трое суток",
        "четверо суток"
    ])
    def test_rental_periods_both_buttons(self, test_user, order_button_type, 
                                       complete_order_from_button, rental_period):
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

    @allure.title("Сравнительный тест - одинаковые данные через разные кнопки")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    def test_same_data_different_buttons(self, test_user, complete_order_from_button):

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
    @allure.title("Проверка видимости и доступности обеих кнопок заказа")
    @pytest.mark.smoke
    @allure.severity(allure.severity_level.CRITICAL)
    def test_both_order_buttons_visibility(self, app,open_main_page):

        
        with allure.step("Проверить доступность обеих кнопок заказа"):
            app.home_page.verify_order_buttons_availability()

    @allure.title("Проверка перехода к форме заказа через обе кнопки")
    @pytest.mark.smoke
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navigation_to_order_form(self, app,open_main_page, order_button_type, click_order_button):
        button_names = {"top": "верхняя", "bottom": "нижняя"}
        button_name = button_names[order_button_type]

        with allure.step(f"Кликнуть по {button_name} кнопке заказа"):
            click_order_button(order_button_type)
        
        with allure.step("Проверить, что отображается форма заказа"):
            app.order_page.verify_order_form_displayed()

    @allure.title("Проверка заполнения первого шага через обе кнопки")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.CRITICAL)
    def test_first_step_completion_both_buttons(self, app,open_main_page, test_user, order_button_type,
                                              click_order_button, fill_order_form_step1):
        button_names = {"top": "верхняя", "bottom": "нижняя"}
        button_name = button_names[order_button_type]
        

        with allure.step(f"Перейти к форме заказа через {button_name} кнопку"):
            click_order_button(order_button_type)
        
        with allure.step(f"Заполнить первый шаг формы (пользователь: {test_user.name})"):
            fill_order_form_step1(test_user, metro_station="Курская")
        
        with allure.step("Проверить переход ко второму шагу"):
            app.order_page.verify_step2_displayed()

    @allure.title("Множественные заказы через разные кнопки")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    def test_multiple_orders_alternating_buttons(self, complete_order_from_button):


        buttons = ["top", "bottom", "top"]
        
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

    @allure.title("Проверка с разными типами пользователей через обе кнопки")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    def test_predefined_users_both_buttons(self, any_user, order_button_type, complete_order_from_button):
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
