from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        #поиск кнопок с выпадающим списком
        self.how_much_button: Locator = self.page.locator("//div[@id='accordion__heading-0']")
        self.several_scooters: Locator = self.page.locator("//div[@id='accordion__heading-1']")
        self.time_arenda: Locator = self.page.locator("//div[@id='accordion__heading-2']")
        self.zakaz_today: Locator = self.page.locator("//div[@id='accordion__heading-3']")
        self.prodlit_and_vernut: Locator = self.page.locator("//div[@id='accordion__heading-4']")
        self.zarydka_on_samokat: Locator = self.page.locator("//div[@id='accordion__heading-5']")
        self.otmena_zakaza: Locator = self.page.locator("//div[@id='accordion__heading-6']")
        self.zamkadish: Locator = self.page.locator("//div[@id='accordion__heading-7']")

        # Поиск выпадающего текста
        self.texts = {
            "how_much": self.page.locator("p:has-text('Сутки — 400 рублей. Оплата курьеру — наличными или картой.')"),
            "several_scooters": self.page.locator(
                "p:has-text('Пока что у нас так: один заказ — один самокат. Если хотите покататься с друзьями, можете просто сделать несколько заказов — один за другим.')"),
            "time_arenda": self.page.locator(
                "p:has-text('Допустим, вы оформляете заказ на 8 мая. Мы привозим самокат 8 мая в течение дня. Отсчёт времени аренды начинается с момента, когда вы оплатите заказ курьеру. Если мы привезли самокат 8 мая в 20:30, суточная аренда закончится 9 мая в 20:30.')"),
            "zakaz_today": self.page.locator(
                "p:has-text('Только начиная с завтрашнего дня. Но скоро станем расторопнее.')"),
            "prodlit_and_vernut": self.page.locator(
                "p:has-text('Пока что нет! Но если что-то срочное — всегда можно позвонить в поддержку по красивому номеру 1010.')"),
            "zarydka_on_samokat": self.page.locator(
                "p:has-text('Самокат приезжает к вам с полной зарядкой. Этого хватает на восемь суток — даже если будете кататься без передышек и во сне. Зарядка не понадобится.')"),
            "otmena_zakaza": self.page.locator(
                "p:has-text('Да, пока самокат не привезли. Штрафа не будет, объяснительной записки тоже не попросим. Все же свои.')"),
            "zamkadish": self.page.locator(
                "p:has-text('Да, обязательно. Всем самокатов! И Москве, и Московской области.')")
        }


