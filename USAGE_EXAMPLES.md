# 🛴 Примеры использования новых фикстур для тестирования заказов

## 📊 Новые возможности UserCredentials

### Расширенная модель пользователя:
```python
@dataclass
class UserCredentials:
    email: str
    password: str
    name: str          # ✨ НОВОЕ
    surname: str       # ✨ НОВОЕ
    address: str       # ✨ НОВОЕ
    
    @classmethod
    def generate_fake(cls):  # ✨ НОВОЕ
        return cls(
            email=fake.email(),
            password=fake.password(),
            name=fake.first_name(),
            surname=fake.surname(),
            address=fake.address()
        )
```

### Типы пользователей:
```python
common_users = {
    "user": UserCredentials(...),              # Статичный
    "admin": UserCredentials(...),             # Статичный  
    "user_order": UserCredentials.generate_fake()  # ✨ Рандомный
}
```

## 🎯 Фикстуры для работы с пользователями

### 1. Рандомный пользователь
```python
def test_example(test_user):
    # Каждый раз новые данные
    print(f"Имя: {test_user.name}")
    print(f"Email: {test_user.email}")
```

### 2. Предопределенный пользователь
```python
def test_example(predefined_user):
    # Всегда user_order из common_users
    print(f"Email: {predefined_user.email}")
```

### 3. Параметризованная фикстура
```python
def test_example(any_user):
    # Запустится 3 раза: user, admin, user_order
    print(f"Тип: {any_user.email}")
```

## 🛒 Фикстуры для заказов

### 1. Заполнение первого шага
```python
def test_example(app, test_user, fill_order_form_step1):
    # Переходим к форме заказа
    app.order_page.one_button_order.click()
    
    # Заполняем личные данные
    fill_order_form_step1(test_user, metro_station="Курская")
```

### 2. Заполнение второго шага
```python
def test_example(app, fill_order_form_step2):
    # ... заполнили первый шаг ...
    
    # Заполняем данные о доставке
    fill_order_form_step2(
        delivery_date="25.12.2024",
        rental_period="двое суток",
        comment="Новогодний заказ"
    )
```

### 3. Полный цикл заказа
```python
def test_example(app, test_user, complete_order_flow):
    # Переходим к форме
    app.order_page.one_button_order.click()
    
    # Полностью оформляем заказ
    complete_order_flow(
        user_data=test_user,
        metro_station="Сокольники",
        delivery_date="15.12.2024",
        rental_period="сутки",
        comment="Быстрый заказ"
    )
```

## 📝 Примеры тестов

### Базовый тест с рандомными данными
```python
def test_order_with_random_user(app, test_user, complete_order_flow):
    app.home_page.open("https://qa-scooter.praktikum-services.ru")
    app.order_page.one_button_order.click()
    
    complete_order_flow(test_user)
    
    expect(app.order_page.order_success_header).to_be_visible()
```

### Параметризованный тест станций метро
```python
@pytest.mark.parametrize("station", ["Курская", "Сокольники", "Комсомольская"])
def test_metro_stations(app, test_user, fill_order_form_step1, station):
    app.home_page.open("https://qa-scooter.praktikum-services.ru")
    app.order_page.one_button_order.click()
    
    fill_order_form_step1(test_user, metro_station=station)
    
    expect(app.order_page.date_input).to_be_visible()
```

### Тест с разными типами пользователей
```python
def test_different_users(app, any_user, fill_order_form_step1):
    # Запустится 3 раза для user, admin, user_order
    app.home_page.open("https://qa-scooter.praktikum-services.ru")
    app.order_page.one_button_order.click()
    
    fill_order_form_step1(any_user)
    
    expect(app.order_page.date_input).to_be_visible()
```

## 🚀 Преимущества новой архитектуры

1. **Гибкость данных**: Рандомные и статичные пользователи
2. **Переиспользование**: Фикстуры можно комбинировать
3. **Читаемость**: Тесты фокусируются на логике, а не на заполнении форм
4. **Масштабируемость**: Легко добавлять новые типы пользователей
5. **Поддержка**: Изменения в одном месте влияют на все тесты

## 📋 Команды для запуска

```bash
# Запуск всех тестов заказа
python3 -m pytest tests/test_order_page.py -v

# Запуск конкретного теста
python3 -m pytest tests/test_order_page.py::TestOrderPage::test_complete_order_flow -v

# Запуск с параметром окружения
python3 -m pytest tests/test_order_page.py --env=dev -v

# Генерация отчета Allure
python3 -m pytest tests/test_order_page.py --alluredir=reports/
allure serve reports/
```
