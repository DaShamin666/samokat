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
        if cookie_consent.is_visible():
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
                    page.locator(selector).click()
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
    Переиспользует метод из HomePage.
    """
    def _click_buttons():
        app.home_page.click_all_accordion_buttons()
    
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
    Переиспользует метод из OrderPage.
    """
    def _fill_form(user_data=None, metro_station="Сокольники"):
        app.order_page.fill_step1_form_simple(metro_station)
    
    return _fill_form

@pytest.fixture
def fill_order_form_step2(app):
    """
    Фикстура для заполнения второго шага формы заказа.
    Переиспользует метод из OrderPage.
    """
    def _fill_form(delivery_date="01.12.2024", rental_period="сутки", comment=""):
        app.order_page.fill_step2_form(delivery_date, rental_period, comment)
        # Подтверждаем заказ
        app.order_page.confirm_button.click(force=True)
    
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
            cookie_accept.wait_for(state='visible')
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

@pytest.fixture
def open_main_page(app,request):
    env_name = request.config.getoption("--env")
    config = environments[env_name]
    with allure.step("открыть главную страницу"):
        app.home_page.open(config.url)
    return app