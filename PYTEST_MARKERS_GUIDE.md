# 🏷️ Руководство по маркам pytest

## 📊 Обзор марок

В проекте применены две основные марки для категоризации тестов:

### 🔥 `@pytest.mark.smoke`
**Назначение**: Критические тесты для smoke testing (быстрая проверка основного функционала)

**Характеристики**:
- ⚡ Быстрые тесты (обычно < 2 секунд)
- 🎯 Критический функционал
- 🔍 Базовая проверка работоспособности
- 🚀 Запускаются в CI/CD на каждом коммите

### 🔄 `@pytest.mark.regression`
**Назначение**: Полные регрессионные тесты (детальная проверка всего функционала)

**Характеристики**:
- 📋 Подробные тесты всех сценариев
- 🔄 Параметризованные тесты
- 🧪 Граничные случаи
- 📈 Запускаются в полном регрессионном цикле

## 📈 Статистика тестов

### Smoke тесты: **9 тестов**
```
✅ Навигация через обе кнопки заказа (2 теста)
✅ Проверка текста на кнопках (1 тест)  
✅ Клики по FAQ аккордеону (1 тест)
✅ Видимость кнопок заказа (1 тест)
✅ Переход к форме заказа (2 теста)
✅ Навигация кнопок верх/низ (2 теста)
```

### Regression тесты: **39 тестов**
```
✅ Сравнение результатов кнопок (1 тест)
✅ Отдельные FAQ кнопки (8 тестов)
✅ Полный путь заказа через кнопки (2 теста)
✅ Разные станции метро (8 тестов)
✅ Разные периоды аренды (8 тестов)
✅ Множественные заказы (1 тест)
✅ Разные пользователи (6 тестов)
✅ Заполнение форм (5 тестов)
```

## 🚀 Команды запуска

### Smoke тесты (быстрая проверка)
```bash
# Запуск всех smoke тестов
python3 -m pytest -m smoke -v

# Smoke тесты с подробным выводом
python3 -m pytest -m smoke -v --tb=short

# Только сбор smoke тестов (без запуска)
python3 -m pytest --collect-only -m smoke -q
```

### Regression тесты (полная проверка)
```bash
# Запуск всех regression тестов
python3 -m pytest -m regression -v

# Regression тесты с ограничением времени
python3 -m pytest -m regression --maxfail=3 -v

# Только сбор regression тестов
python3 -m pytest --collect-only -m regression -q
```

### Комбинированные запуски
```bash
# Запуск только smoke тестов (исключая regression)
python3 -m pytest -m "smoke and not regression" -v

# Запуск всех тестов кроме regression
python3 -m pytest -m "not regression" -v

# Запуск и smoke, и regression
python3 -m pytest -m "smoke or regression" -v

# Все тесты без фильтрации
python3 -m pytest -v
```

## 📋 Распределение марок по файлам

### `test_buttons_demo.py`
- ✅ **Smoke**: `test_both_buttons_navigation_demo`, `test_buttons_text`
- 🔄 **Regression**: `test_buttons_lead_to_same_form`

### `test_click_on_button_text_visible.py`
- ✅ **Smoke**: `test_click_all_accordion_buttons_and_check_text_visibility`
- 🔄 **Regression**: `test_individual_accordion_button` (8 параметризованных)

### `test_full_order_path.py`
- ✅ **Smoke**: `test_both_order_buttons_visibility`, `test_navigation_to_order_form`
- 🔄 **Regression**: все остальные тесты полного пути заказа

### `test_order_page.py`
- ✅ **Smoke**: `test_order_button_top_navigation`, `test_order_button_bottom_navigation`
- 🔄 **Regression**: `test_fill_order_form_step1_random_user`, `test_complete_order_flow`

## ⚙️ Конфигурация pytest.ini

```ini
[pytest]
markers =
    smoke: критические тесты для smoke testing (быстрая проверка основного функционала)
    regression: полные регрессионные тесты (детальная проверка всего функционала)
    
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --tb=short
    --durations=10
```

## 🎯 Стратегия использования

### Разработка (Development)
```bash
# Быстрая проверка после изменений
python3 -m pytest -m smoke

# Результат: 9 тестов за ~10 секунд
```

### Pre-commit хуки
```bash
# В хуке перед коммитом
python3 -m pytest -m smoke --maxfail=1

# Прерывается на первой ошибке
```

### Pull Request проверка
```bash
# Полная регрессия для PR
python3 -m pytest -m regression

# Результат: 39 тестов полной проверки
```

### Release проверка
```bash
# Все тесты перед релизом
python3 -m pytest

# Результат: все 65 тестов
```

## 📊 Время выполнения

| Марка | Количество | Среднее время | Применение |
|-------|------------|---------------|------------|
| **smoke** | 9 тестов | ~10 сек | Ежедневная разработка |
| **regression** | 39 тестов | ~60+ сек | PR и релиз |
| **все тесты** | 65 тестов | ~90+ сек | Полная проверка |

## 🔍 Проверка марок

```bash
# Посмотреть все доступные марки
python3 -m pytest --markers

# Проверить количество smoke тестов
python3 -m pytest --collect-only -m smoke -q | grep selected

# Проверить количество regression тестов  
python3 -m pytest --collect-only -m regression -q | grep selected
```

## ✨ Преимущества системы марок

1. **🚀 Скорость разработки**: Быстрая обратная связь с smoke тестами
2. **🎯 Гибкость запуска**: Выбор подходящего набора тестов
3. **📊 Ясная структура**: Понятное разделение по критичности
4. **🔄 CI/CD интеграция**: Разные стратегии для разных этапов
5. **📈 Масштабируемость**: Легко добавлять новые марки при росте проекта

## 🎉 Готовые команды для копирования

```bash
# Ежедневная разработка
python3 -m pytest -m smoke -v

# Перед коммитом
python3 -m pytest -m smoke --tb=short

# Проверка PR
python3 -m pytest -m regression -v

# Полная проверка релиза
python3 -m pytest -v

# Отладка конкретной марки
python3 -m pytest -m smoke --pdb -s
```

Система марок готова к использованию! 🎯
