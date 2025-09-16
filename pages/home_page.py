from playwright.sync_api import Page, Locator,expect
from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        
        self.order_button_top: Locator = self.page.locator("button.Button_Button__ra12g:has-text('Заказать')").first
        self.order_button_bottom: Locator = self.page.locator("button.Button_Button__ra12g.Button_Middle__1CSJM:has-text('Заказать')")
        
        self.how_much_button: Locator = self.page.locator("//div[@id='accordion__heading-0']")
        self.several_scooters: Locator = self.page.locator("//div[@id='accordion__heading-1']")
        self.time_arenda: Locator = self.page.locator("//div[@id='accordion__heading-2']")
        self.zakaz_today: Locator = self.page.locator("//div[@id='accordion__heading-3']")
        self.prodlit_and_vernut: Locator = self.page.locator("//div[@id='accordion__heading-4']")
        self.zarydka_on_samokat: Locator = self.page.locator("//div[@id='accordion__heading-5']")
        self.otmena_zakaza: Locator = self.page.locator("//div[@id='accordion__heading-6']")
        self.zamkadish: Locator = self.page.locator("//div[@id='accordion__heading-7']")

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

    def click_all_accordion_buttons(self):
        """Кликает по всем кнопкам аккордеона и проверяет отображение текстов."""

        self.how_much_button.click()
        expect(self.how_much_button).to_be_visible()
        expect(self.texts["how_much"]).to_be_visible()

        self.several_scooters.click()
        expect(self.several_scooters).to_be_visible()
        expect(self.texts["several_scooters"]).to_be_visible()

        self.time_arenda.click()
        expect(self.time_arenda).to_be_visible()
        expect(self.texts["time_arenda"]).to_be_visible()

        self.zakaz_today.click()
        expect(self.zakaz_today).to_be_visible()
        expect(self.texts["zakaz_today"]).to_be_visible()

        self.prodlit_and_vernut.click()
        expect(self.prodlit_and_vernut).to_be_visible()
        expect(self.texts["prodlit_and_vernut"]).to_be_visible()

        self.zarydka_on_samokat.click()
        expect(self.zarydka_on_samokat).to_be_visible()
        expect(self.texts["zarydka_on_samokat"]).to_be_visible()

        self.otmena_zakaza.click()
        expect(self.otmena_zakaza).to_be_visible()
        expect(self.texts["otmena_zakaza"]).to_be_visible()

        self.zamkadish.click()
        expect(self.zamkadish).to_be_visible()
        expect(self.texts["zamkadish"]).to_be_visible()

    def click_accordion_button_by_key(self, button_key: str, text_key: str):
        """Кликает по отдельной кнопке аккордеона и проверяет отображение текста."""

        button = getattr(self, button_key)
        button.click()
        
        expect(button).to_be_visible()
        expect(self.texts[text_key]).to_be_visible()

    def navigate_to_order_form_via_top_button(self):
        """Переходит к форме заказа через верхнюю кнопку."""
        self.order_button_top.click()

    def navigate_to_order_form_via_bottom_button(self):
        """Переходит к форме заказа через нижнюю кнопку."""
        self.order_button_bottom.scroll_into_view_if_needed()
        self.order_button_bottom.click()

    def verify_order_buttons_availability(self):
        """Проверяет доступность обеих кнопок заказа."""
        expect(self.order_button_top).to_be_visible()
        expect(self.order_button_top).to_be_enabled()
        self.order_button_bottom.scroll_into_view_if_needed()
        expect(self.order_button_bottom).to_be_visible()
        expect(self.order_button_bottom).to_be_enabled()

    def verify_order_buttons_text(self):
        """Проверяет текст на кнопках заказа."""
        expect(self.order_button_top).to_have_text("Заказать")
        self.order_button_bottom.scroll_into_view_if_needed()
        expect(self.order_button_bottom).to_have_text("Заказать")

    def verify_order_form_navigation(self):
        """Проверяет, что произошел переход к форме заказа."""
        # Этот метод будет использоваться после клика по кнопке заказа
        # Проверка будет в OrderPage, так как форма заказа там
        pass

