import pytest
import allure
from playwright.sync_api import Page, expect
from config.application import Application
from config.environments import *


# ============================================================
#
#   Хуки Pytest (Настройка и отчетность)
#
# ============================================================

def pytest_addoption(parser):
    """Добавляем опции для выбора окружения и типа пользователя."""
    parser.addoption("--env", default="dev", choices=[e.value for e in Environment],
                     help="Выберите окружение: dev или stage")
    parser.addoption("--user-type", default=None, choices=common_users.keys(),
                     help="Выберите тип пользователя: user или admin")

def pytest_configure(config):
    """Выводит информацию о тестовом окружении перед запуском."""
    env_name = config.getoption("--env")
    user_type = config.getoption("--user-type")
    print_environment_info(env_name, user_type)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Создает скриншот в Allure при падении теста."""
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call' and report.failed:
        try:
            page = item.funcargs['page']
            allure.attach(
                page.screenshot(full_page=True), name=f"screenshot_{item.nodeid}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")


# ============================================================
#
#   Фикстуры для тестирования
#
# ============================================================

@pytest.fixture
def app(page: Page):
    """Фикстура для работы с приложением."""
    app = Application(page)
    
    # Обработка cookie consent баннера если он есть
    try:
        cookie_consent = page.locator("div.App_CookieConsent__1yUIN")
        if cookie_consent.is_visible(timeout=2000):
            # Ищем кнопку принятия cookies (может быть разные варианты)
            accept_buttons = [
                "button:has-text('Принять')",
                "button:has-text('Accept')", 
                "button:has-text('OK')",
                "[data-accept-cookies]",
                ".cookie-accept"
            ]
            for selector in accept_buttons:
                try:
                    page.locator(selector).click(timeout=1000)
                    break
                except:
                    continue
    except:
        pass  # Игнорируем если баннера нет
    
    return app

@pytest.fixture
def click_accordion_buttons(app):
    """
    Фикстура для тестирования кликов по кнопкам аккордеона.
    Возвращает функцию, которая выполняет клики и проверки для всех кнопок FAQ.
    """
    def _click_buttons():
        home_page = app.home_page
        
        # Клик по кнопке "Сколько это стоит? И как оплатить?"
        home_page.how_much_button.click()
        expect(home_page.how_much_button).to_be_visible()
        expect(home_page.texts["how_much"]).to_be_visible()

        # Клик по кнопке "Хочу заказать несколько самокатов"
        home_page.several_scooters.click()
        expect(home_page.several_scooters).to_be_visible()
        expect(home_page.texts["several_scooters"]).to_be_visible()

        # Клик по кнопке "Как рассчитывается время аренды?"
        home_page.time_arenda.click()
        expect(home_page.time_arenda).to_be_visible()
        expect(home_page.texts["time_arenda"]).to_be_visible()

        # Клик по кнопке "Можно ли заказать самокат прямо на сегодня?"
        home_page.zakaz_today.click()
        expect(home_page.zakaz_today).to_be_visible()
        expect(home_page.texts["zakaz_today"]).to_be_visible()

        # Клик по кнопке "Можно ли продлить заказ или вернуть самокат раньше?"
        home_page.prodlit_and_vernut.click()
        expect(home_page.prodlit_and_vernut).to_be_visible()
        expect(home_page.texts["prodlit_and_vernut"]).to_be_visible()

        # Клик по кнопке "Вы привозите зарядку вместе с самокатом?"
        home_page.zarydka_on_samokat.click()
        expect(home_page.zarydka_on_samokat).to_be_visible()
        expect(home_page.texts["zarydka_on_samokat"]).to_be_visible()

        # Клик по кнопке "Можно ли отменить заказ?"
        home_page.otmena_zakaza.click()
        expect(home_page.otmena_zakaza).to_be_visible()
        expect(home_page.texts["otmena_zakaza"]).to_be_visible()

        # Клик по кнопке "Я живу за МКАДом, привезёте?"
        home_page.zamkadish.click()
        expect(home_page.zamkadish).to_be_visible()
        expect(home_page.texts["zamkadish"]).to_be_visible()
    
    return _click_buttons


# ============================================================
#
#   Фикстуры для работы с пользователями и заказами
#
# ============================================================

@pytest.fixture
def test_user():
    """
    Фикстура для получения тестового пользователя с рандомными данными.
    Каждый раз возвращает нового пользователя с уникальными данными.
    """
    from config.environments import UserCredentials
    return UserCredentials.generate_fake()

@pytest.fixture
def predefined_user():
    """
    Фикстура для получения предопределенного пользователя для заказов.
    """
    from config.environments import common_users
    return common_users["user_order"]

@pytest.fixture(params=["user", "admin", "user_order"])
def any_user(request):
    """
    Параметризованная фикстура для тестирования с разными типами пользователей.
    """
    from config.environments import common_users
    return common_users[request.param]

@pytest.fixture
def fill_order_form_step1(app):
    """
    Фикстура для заполнения первого шага формы заказа.
    Возвращает функцию, которая принимает пользователя и заполняет форму.
    """
    def _fill_form(user_data, metro_station="Сокольники"):
        order_page = app.order_page
        
        # Заполняем личные данные с диагностикой
        print(f"DEBUG: Filling name: {user_data.name}")
        order_page.name_input.fill(user_data.name)
        
        print(f"DEBUG: Filling surname: {user_data.surname}")
        order_page.surname_input.fill(user_data.surname)
        
        # Используем более простой адрес без переносов строк
        simple_address = user_data.address.replace('\n', ' ').strip()
        print(f"DEBUG: Filling address: {simple_address}")
        order_page.adres_input.fill(simple_address)
        
        # Выбираем станцию метро
        print(f"DEBUG: Selecting metro station: {metro_station}")
        order_page.select_metro_station(metro_station)
        
        # Вводим телефон
        print("DEBUG: Filling phone number")
        order_page.phone_input.fill("+79991234567")  # Можно добавить в UserCredentials
        
        # Проверяем значения всех полей после заполнения
        print("DEBUG: Verifying filled values:")
        try:
            name_value = order_page.name_input.input_value()
            surname_value = order_page.surname_input.input_value()
            address_value = order_page.adres_input.input_value()
            phone_value = order_page.phone_input.input_value()
            metro_value = order_page.metro_input.input_value()
            
            print(f"DEBUG: Name field value: '{name_value}'")
            print(f"DEBUG: Surname field value: '{surname_value}'")
            print(f"DEBUG: Address field value: '{address_value}'")
            print(f"DEBUG: Phone field value: '{phone_value}'")
            print(f"DEBUG: Metro field value: '{metro_value}'")
        except Exception as e:
            print(f"DEBUG: Error getting field values: {e}")
        
        # Нажимаем "Далее" (force=True чтобы обойти cookie consent)
        order_page.next_button.click(force=True)
        
        # Ждем исчезновения элементов первого шага и появления элементов второго шага
        app.page.wait_for_load_state('networkidle')
        
        # Дополнительная проверка, что мы перешли ко второму шагу
        try:
            # Ждем появления любого элемента второго шага (более надежно, чем конкретный заголовок)
            app.page.locator("input[placeholder='* Когда привезти самокат']").wait_for(state='visible', timeout=10000)
        except Exception as e:
            print(f"DEBUG: Failed to find second step elements after clicking Next")
            print(f"DEBUG: Current URL: {app.page.url}")
            print(f"DEBUG: Page title: {app.page.title()}")
            
            # Диагностика всех кнопок на странице
            all_buttons = app.page.locator("button").all()
            print(f"DEBUG: Found {len(all_buttons)} buttons on page")
            for i, btn in enumerate(all_buttons):
                try:
                    text = btn.text_content() or ""
                    visible = btn.is_visible()
                    enabled = btn.is_enabled()
                    print(f"DEBUG: Button {i}: '{text}' (visible: {visible}, enabled: {enabled})")
                except:
                    print(f"DEBUG: Button {i}: Error getting info")
            
            # Проверяем ошибки валидации
            print("DEBUG: Checking for validation errors...")
            error_elements = app.page.locator(".Input_ErrorMessage__3HHxB, .Input_Error__1RWCy").all()
            for i, error in enumerate(error_elements):
                try:
                    text = error.text_content()
                    visible = error.is_visible()
                    if visible and text:
                        print(f"DEBUG: Validation error {i}: '{text}'")
                except:
                    pass
            
            # Пытаемся кликнуть "Далее" еще раз, если не перешли
            if order_page.next_button.is_visible():
                print("DEBUG: Next button still visible, clicking again")
                order_page.next_button.click(force=True)
                app.page.wait_for_load_state('networkidle')
                app.page.locator("input[placeholder='* Когда привезти самокат']").wait_for(state='visible', timeout=10000)
            else:
                print("DEBUG: Next button is not visible, can't click again")
                raise e
    
    return _fill_form

@pytest.fixture
def fill_order_form_step2(app):
    """
    Фикстура для заполнения второго шага формы заказа.
    """
    def _fill_form(delivery_date="01.12.2024", rental_period="сутки", comment=""):
        order_page = app.order_page
        
        # Дополнительное ожидание стабилизации страницы
        app.page.wait_for_load_state('networkidle')
        
        # Ждем появления заголовка "Про аренду" (второй шаг) с увеличенным таймаутом
        pro_arendu_header = app.page.locator("div.Order_Header__BZXOb:has-text('Про аренду')")
        try:
            pro_arendu_header.wait_for(state='visible', timeout=30000)
        except Exception as e:
            # Дополнительная диагностика при ошибке
            print(f"DEBUG: Current URL: {app.page.url}")
            print(f"DEBUG: Page title: {app.page.title()}")
            all_headers = app.page.locator("div.Order_Header__BZXOb").all()
            print(f"DEBUG: Found {len(all_headers)} Order headers")
            for i, header in enumerate(all_headers):
                try:
                    text = header.text_content()
                    print(f"DEBUG: Header {i}: '{text}'")
                except:
                    print(f"DEBUG: Header {i}: Unable to get text")
            raise e
        
        # Заполняем дату доставки
        order_page.enter_date(delivery_date)
        
        # Выбираем срок аренды
        order_page.select_rental_period(rental_period)
        
        # Выбираем цвет (чекбокс)
        order_page.checkbox.check()
        
        # Добавляем комментарий (если есть)
        if comment:
            order_page.comment_input.fill(comment)
        
        # Подтверждаем заказ (force=True чтобы обойти возможные проблемы)
        order_page.confirm_button.click(force=True)
    
    return _fill_form

@pytest.fixture
def complete_order_flow(app, fill_order_form_step1, fill_order_form_step2):
    """
    Фикстура для полного цикла оформления заказа.
    """
    def _complete_order(user_data, metro_station="Сокольники", 
                       delivery_date="01.12.2024", rental_period="сутки", 
                       comment="Тестовый заказ"):
        
        # Шаг 1: Заполняем личные данные
        fill_order_form_step1(user_data, metro_station)
        
        # Шаг 2: Заполняем данные о доставке
        fill_order_form_step2(delivery_date, rental_period, comment)
    
    return _complete_order

@pytest.fixture(params=["top", "bottom"])
def order_button_type(request):
    """
    Параметризованная фикстура для тестирования обеих кнопок заказа.
    Возвращает тип кнопки: 'top' или 'bottom'.
    """
    return request.param

@pytest.fixture
def click_order_button(app):
    """
    Фикстура для клика по кнопке заказа в зависимости от типа.
    Возвращает функцию, которая принимает тип кнопки и кликает по соответствующей кнопке.
    """
    def _click_button(button_type: str):
        if button_type == "top":
            # Клик по верхней кнопке
            app.order_page.one_button_order.click()
        elif button_type == "bottom":
            # Прокрутка к нижней кнопке и клик
            app.order_page.second_button_order.scroll_into_view_if_needed()
            app.order_page.second_button_order.click()
        else:
            raise ValueError(f"Неизвестный тип кнопки: {button_type}")
    
    return _click_button

@pytest.fixture
def complete_order_from_button(app, click_order_button, complete_order_flow):
    """
    Фикстура для полного цикла заказа, начиная с указанной кнопки.
    """
    def _complete_from_button(button_type: str, user_data, metro_station="Сокольники", 
                             delivery_date="01.12.2024", rental_period="сутки", 
                             comment="Тестовый заказ"):
        
        # Открываем главную страницу
        from config.environments import Environment, environments
        env_config = environments[Environment.DEV]
        app.home_page.open(env_config.url)
        
        # Обработка cookie consent баннера если он появился
        try:
            cookie_accept = app.page.locator("button#rcc-confirm-button")
            cookie_accept.wait_for(state='visible', timeout=3000)
            cookie_accept.click()
        except:
            pass
        
        # Кликаем по нужной кнопке заказа
        click_order_button(button_type)
        
        # Выполняем полный цикл заказа
        complete_order_flow(user_data, metro_station, delivery_date, rental_period, comment)
        
        # Проверяем успешное завершение заказа
        expect(app.order_page.order_success_header).to_be_visible()
    
    return _complete_from_button