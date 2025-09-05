from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.order_page import OrderPage


class Application:
    def __init__(self, page: Page):
        self.page = page

        # Инициализируем все наши Page Objects здесь
        self.home_page = HomePage(self.page)
        self.order_page = OrderPage(self.page)