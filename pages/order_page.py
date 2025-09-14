from pages.base_page import BasePage
from playwright.sync_api import Page, Locator


class OrderPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        #кноки заказа на главной странице
        self.one_button_order:Locator = self.page.locator("button.Button_Button__ra12g:has-text('Заказать')").first
        self.second_button_order:Locator = self.page.locator("button.Button_Button__ra12g.Button_Middle__1CSJM:has-text('Заказать')")


        #локаторы формы заказа
        self.name_input:Locator = self.page.locator("input.Input_Input__1iN_Z.Input_Responsible__1jDKN[placeholder='* Имя']")
        self.surname_input:Locator = self.page.locator("input.Input_Input__1iN_Z.Input_Responsible__1jDKN[placeholder='* Фамилия']")
        self.adres_input:Locator = self.page.locator("input.Input_Input__1iN_Z.Input_Responsible__1jDKN[placeholder='* Адрес: куда привезти заказ']")
        self.metro_input:Locator = self.page.locator("input.select-search__input[placeholder='* Станция метро']")
        self.metro_choice: Locator = self.page.locator("button.select-search__option")
        #использовать в фикстуре для выбора нужной станции
        # def select_station(self, station_name: str):
        #     # Открытие выпадающего списка
        #     self.metro_input.click()
        #
        #     # Выбор станции
        #     self.metro_choice.locator(f"text='{station_name}'").click()  # Клик на нужную станцию
        self.phone_input: Locator = self.page.locator("input[placeholder='* Телефон: на него позвонит курьер']")
        self.next_button: Locator = self.page.locator("button.Button_Button__ra12g.Button_Middle__1CSJM:has-text('Далее')")

        #локаторы данные про аренду
        self.date_input: Locator = self.page.locator("input[placeholder='* Когда привезти самокат']")
        # def enter_date(self, date: str):
        #     # Ввод даты
        #     self.date_input.fill(date)  # Заполнение поля ввода даты
        self.rental_period_option: Locator = self.page.locator("div.Dropdown-option")
        # def select_rental_period(self, period_name: str): использовать в фикстуре
        #     # Открытие выпадающего списка срока аренды
        #     self.rental_period_dropdown.click()
        #
        #     # Выбор срока аренды
        #     self.rental_period_option.locator(f"text='{period_name}'").click()  # Клик на нужный срок аренды
        self.checkbox: Locator = self.page.locator("input#grey")
        self.comment_input: Locator = self.page.locator("input[placeholder='Комментарий для курьера']")
        self.confirm_button: Locator = self.page.locator("button.Button_Button__ra12g.Button_Middle__1CSJM")
        
        # Дополнительные локаторы
        self.rental_period_dropdown: Locator = self.page.locator("div.Dropdown-placeholder")
        self.order_success_header: Locator = self.page.locator("div.Order_Header__BZXOb")
        
    def select_metro_station(self, station_name: str):
        """Выбирает станцию метро из выпадающего списка."""
        # Кликаем по полю ввода станции метро
        self.metro_input.click()
        
        # Ждем появления выпадающего списка
        self.page.wait_for_timeout(1000)
        
        # Выбираем нужную станцию
        station_option = self.metro_choice.locator(f"text='{station_name}'")
        station_option.wait_for(state='visible', timeout=5000)
        station_option.click()
        
        # Ждем закрытия выпадающего списка
        self.page.wait_for_timeout(500)
    
    def enter_date(self, date: str):
        """Вводит дату доставки."""
        # Ждем, пока поле станет доступным для ввода
        self.date_input.wait_for(state='visible', timeout=10000)
        
        # Кликаем по полю перед заполнением
        self.date_input.click()
        
        # Заполняем дату с force=True для надежности
        self.date_input.fill(date, force=True)
        
        # Закрываем календарь, кликнув в другое место
        self.page.click("body")
        self.page.wait_for_timeout(500)  # Небольшая пауза для закрытия календаря
        
    def select_rental_period(self, period_name: str):
        """Выбирает срок аренды из выпадающего списка."""
        self.rental_period_dropdown.click(force=True)
        self.rental_period_option.locator(f"text='{period_name}'").click()