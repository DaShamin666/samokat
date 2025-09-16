from pages.base_page import BasePage
from playwright.sync_api import Page, Locator, expect


class OrderPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.one_button_order:Locator = self.page.locator("button.Button_Button__ra12g:has-text('Заказать')").first
        self.second_button_order:Locator = self.page.locator("button.Button_Button__ra12g.Button_Middle__1CSJM:has-text('Заказать')")


        self.name_input:Locator = self.page.locator("input.Input_Input__1iN_Z.Input_Responsible__1jDKN[placeholder='* Имя']")
        self.surname_input:Locator = self.page.locator("input.Input_Input__1iN_Z.Input_Responsible__1jDKN[placeholder='* Фамилия']")
        self.adres_input:Locator = self.page.locator("input.Input_Input__1iN_Z.Input_Responsible__1jDKN[placeholder='* Адрес: куда привезти заказ']")
        self.metro_input:Locator = self.page.locator("input.select-search__input[placeholder='* Станция метро']")
        self.metro_choice: Locator = self.page.locator("button.select-search__option")

        self.phone_input: Locator = self.page.locator("input[placeholder='* Телефон: на него позвонит курьер']")
        self.next_button: Locator = self.page.locator("button.Button_Button__ra12g.Button_Middle__1CSJM:has-text('Далее')")

        self.date_input: Locator = self.page.locator("input[placeholder='* Когда привезти самокат']")

        self.rental_period_option: Locator = self.page.locator("div.Dropdown-option")

        self.checkbox: Locator = self.page.locator("input#grey")
        self.comment_input: Locator = self.page.locator("input[placeholder='Комментарий для курьера']")
        self.confirm_button: Locator = self.page.locator("button.Button_Button__ra12g.Button_Middle__1CSJM:has-text('Заказать'):not(:has-text('Назад'))")
        
        self.rental_period_dropdown: Locator = self.page.locator("div.Dropdown-placeholder")
        self.order_success_header: Locator = self.page.locator("div.Order_Header__BZXOb")
        
    def select_metro_station(self, station_name: str):

        # Кликаем по полю метро
        self.metro_input.click()
        
        # Ждем появления опций и выбираем нужную станцию
        station_option = self.metro_choice.locator(f"text='{station_name}'")
        station_option.wait_for(state='visible')
        station_option.click()
        
        # Проверяем, что станция выбрана
        expect(self.metro_input).to_have_value(station_name)
    
    def enter_date(self, date: str):
        self.date_input.wait_for(state='visible')
        
        self.date_input.click()
        
        self.date_input.fill(date, force=True)
        
        self.page.click("body")
        
    def select_rental_period(self, period_name: str):
        """Выбирает срок аренды из выпадающего списка."""
        self.rental_period_dropdown.click(force=True)
        self.rental_period_option.locator(f"text='{period_name}'").click()

    def fill_step1_form(self, user_data, metro_station="Сокольники"):
        """Заполняет первый шаг формы заказа."""

        name = "Иван" if not hasattr(user_data, 'name') or not user_data.name else user_data.name
        surname = "Иванов" if not hasattr(user_data, 'surname') or not user_data.surname else user_data.surname
        address = "ул. Тестовая, д. 1" if not hasattr(user_data, 'address') or not user_data.address else user_data.address.replace('\n', ' ').strip()
        
        self.name_input.fill(name)
        self.surname_input.fill(surname)
        self.adres_input.fill(address)
        
        self.select_metro_station(metro_station)
        
        self.phone_input.fill("+79991234567")
        
        expect(self.name_input).to_have_value(name)
        expect(self.surname_input).to_have_value(surname)
        expect(self.adres_input).to_have_value(address)
        expect(self.phone_input).to_have_value("+79991234567")
        
        expect(self.next_button).to_be_visible()
        expect(self.next_button).to_be_enabled()
        
        self.next_button.click(force=True)
        
        self.page.wait_for_load_state('networkidle')
        
        expect(self.date_input).to_be_visible()

    def fill_step2_form(self, delivery_date="01.12.2024", rental_period="сутки", comment=""):
        """Заполняет второй шаг формы заказа."""

        self.page.wait_for_load_state('networkidle')
        
        pro_arendu_header = self.page.locator("div.Order_Header__BZXOb:has-text('Про аренду')")
        expect(pro_arendu_header).to_be_visible()
        
        self.enter_date(delivery_date)
        
        self.select_rental_period(rental_period)
        
        expect(self.checkbox).to_be_visible()
        self.checkbox.check()
        expect(self.checkbox).to_be_checked()
        
        if comment:
            self.comment_input.fill(comment)
            expect(self.comment_input).to_have_value(comment)


    def fill_minimal_demo_data(self, button_name: str = ""):
        """Заполняет минимальные данные для демонстрационных тестов."""

        self.name_input.fill("Иван")
        self.surname_input.fill("Иванов")
        self.adres_input.fill("ул. Тестовая, д. 1")
        
        self.metro_input.click()
        self.metro_choice.first.click()
        
        self.phone_input.fill("+79991234567")
        
        expect(self.name_input).to_have_value("Иван")
        expect(self.surname_input).to_have_value("Иванов")
        expect(self.phone_input).to_have_value("+79991234567")

    def click_next_button(self):
        """Кликает по кнопке 'Далее'."""
        self.next_button.click()

    def fill_step1_form_simple(self, metro_station="Сокольники"):
        """Заполняет первый шаг формы заказа простыми данными."""

        self.name_input.fill("Иван")
        self.surname_input.fill("Иванов")
        self.adres_input.fill("ул. Тестовая, д. 1")
        self.phone_input.fill("+79991234567")
        
        self.metro_input.click()
        self.metro_choice.locator(f"text='{metro_station}'").click()
        
        expect(self.name_input).to_have_value("Иван")
        expect(self.surname_input).to_have_value("Иванов")
        expect(self.adres_input).to_have_value("ул. Тестовая, д. 1")
        expect(self.phone_input).to_have_value("+79991234567")
        
        expect(self.next_button).to_be_enabled()
        self.next_button.click()
        
        self.page.wait_for_load_state('networkidle')
        
        try:
            expect(self.date_input).to_be_visible()
            return True
        except:
            return False

    def verify_order_form_displayed(self):
        """Проверяет, что форма заказа отображается."""
        expect(self.name_input).to_be_visible()

    def verify_step2_displayed(self):
        """Проверяет, что отображается второй шаг формы."""
        expect(self.date_input).to_be_visible()

    def verify_order_success(self):
        """Проверяет успешное оформление заказа."""
        expect(self.order_success_header).to_be_visible()

    def verify_form_validation_failed(self):
        """Проверяет, что валидация формы не прошла (остались на первом шаге)."""
        expect(self.name_input).to_be_visible()