from playwright.sync_api import Page, expect, Locator

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, path: str = "/"):
        """Открывает страницу по указанному пути."""
        self.page.goto(path)

    def check_url_contains(self, path: str):
        """Проверяет, что текущий URL содержит указанный путь."""
        expect(self.page).to_have_url(path)


