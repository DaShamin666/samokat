# 🛴 Samokat E2E Testing Framework

[![🧪 Automated Testing](https://github.com/username/samokat-tests/actions/workflows/tests.yml/badge.svg)](https://github.com/username/samokat-tests/actions/workflows/tests.yml)
[![🌙 Nightly Tests](https://github.com/username/samokat-tests/actions/workflows/nightly.yml/badge.svg)](https://github.com/username/samokat-tests/actions/workflows/nightly.yml)

Комплексная система автоматизированного тестирования для веб-приложения Samokat с использованием Playwright и pytest.

## 🚀 Быстрый старт

### Установка
```bash
# Клонирование репозитория
git clone <repo-url>
cd samokat-tests

# Установка зависимостей
pip install -r requirements.txt

# Установка браузеров
playwright install
```

### Запуск тестов
```bash
# Быстрая проверка (smoke тесты)
python -m pytest -m smoke -v

# Полное тестирование (regression)
python -m pytest -m regression -v

# Все тесты
python -m pytest -v
```

## 📊 Структура тестов

- **🔥 Smoke Tests**: 9 критических тестов (~10 сек)
- **🔄 Regression Tests**: 39 полных тестов (~30 мин)
- **🎯 Total Coverage**: 65 тестов всех сценариев

## 🎭 Поддерживаемые браузеры

- ✅ Chromium
- ✅ Firefox  
- ✅ WebKit (Safari)

## 🧪 Тестируемый функционал

### Навигация и кнопки заказа
- ✅ Проверка обеих кнопок "Заказать" (верхняя/нижняя)
- ✅ Переход к форме заказа
- ✅ Видимость и доступность элементов

### FAQ аккордеон
- ✅ Клики по всем 8 кнопкам FAQ
- ✅ Отображение соответствующих текстов
- ✅ Индивидуальная проверка каждой кнопки

### Форма заказа
- ✅ Заполнение личных данных
- ✅ Выбор станций метро
- ✅ Различные периоды аренды
- ✅ Полный цикл оформления заказа

### Пользовательские данные
- ✅ Рандомные пользователи (Faker)
- ✅ Предопределенные пользователи
- ✅ Параметризованное тестирование

## 🔧 Архитектура

```
├── .github/workflows/     # CI/CD автоматизация
├── config/               # Конфигурация окружений
├── pages/                # Page Object Model
├── tests/                # Тестовые сценарии  
├── conftest.py           # Фикстуры pytest
└── pytest.ini           # Настройки pytest
```

## 🏷️ Марки тестов

- `@pytest.mark.smoke` - Критические тесты для быстрой проверки
- `@pytest.mark.regression` - Полные регрессионные тесты

```bash
# Только smoke тесты
python -m pytest -m smoke

# Только regression тесты  
python -m pytest -m regression
```

## 🚀 CI/CD Pipeline

### Pull Request Flow
1. **🔥 Smoke Tests** - Быстрая проверка (10 сек)
2. **🔄 Regression Tests** - Полное тестирование (30 мин)
3. **🎯 Full Test Suite** - Финальная проверка (45 мин)

### Автоматические запуски
- ✅ Pull Request → Полная проверка
- ✅ Push в main → Быстрая проверка  
- ✅ Nightly → Полное тестирование на всех браузерах

## 📈 Отчеты

- **GitHub Actions**: Встроенные отчеты и статистика
- **Allure Reports**: Подробные отчеты с скриншотами
- **Artifacts**: Скриншоты при ошибках

## 🛠️ Разработка

### Добавление новых тестов
1. Создать тест в соответствующем файле
2. Добавить подходящую марку (`@pytest.mark.smoke` или `@pytest.mark.regression`)
3. Использовать существующие фикстуры
4. Создать Pull Request

### Структура тестов
```python
@pytest.mark.smoke
@allure.title("Описание теста")
@allure.description("Подробное описание")
@allure.severity(allure.severity_level.CRITICAL)
def test_example(app, test_user):
    # Тестовый код
    pass
```



## 🤝 Контрибьюция

1. Fork репозитория
2. Создать feature branch
3. Добавить тесты
4. Создать Pull Request
5. Дождаться прохождения CI/CD

## 📊 Статистика

- **Общее покрытие**: 65 тестов
- **Время выполнения**: 
  - Smoke: ~10 секунд
  - Regression: ~30 минут
  - Full: ~45 минут
- **Браузеры**: 3 (Chromium, Firefox, WebKit)
- **Окружения**: 2 (dev, stage)

---

Made with ❤️ for automated testing
