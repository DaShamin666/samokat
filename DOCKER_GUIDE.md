# 🐳 Docker Guide для тестов Samokat

Руководство по запуску и использованию Docker-окружения для автоматизированного тестирования проекта Samokat.

## 🚀 Быстрый старт

### Установка Docker
Убедитесь, что у вас установлены Docker и Docker Compose:
```bash
# Проверка установки
docker --version
docker-compose --version
```

### Первый запуск
```bash
# Сборка образа
./run-docker-tests.sh build

# Запуск smoke тестов
./run-docker-tests.sh smoke
```

## 📋 Доступные команды

### Основные команды

| Команда | Описание | Время выполнения |
|---------|----------|------------------|
| `build` | Собрать Docker образ | ~5-10 мин |
| `smoke` | Запустить smoke тесты | ~10 сек |
| `regression` | Запустить regression тесты | ~30 мин |
| `full` | Запустить все тесты | ~45 мин |
| `parallel` | Параллельный запуск тестов | ~15 мин |

### Служебные команды

| Команда | Описание |
|---------|----------|
| `allure` | Запустить Allure сервер |
| `clean` | Очистить контейнеры и образы |
| `logs` | Показать логи последнего запуска |
| `shell` | Войти в контейнер для отладки |

## 🛠️ Параметры запуска

### Опции командной строки

```bash
# Выбор окружения
./run-docker-tests.sh smoke --env=dev     # Dev окружение (по умолчанию)
./run-docker-tests.sh smoke --env=stage   # Stage окружение

# Дополнительные аргументы для pytest
./run-docker-tests.sh full --args='-k test_order -v'

# Пересборка образа перед запуском
./run-docker-tests.sh regression --rebuild

# Комбинирование параметров
./run-docker-tests.sh parallel --env=stage --args='-m smoke' --rebuild
```

### Переменные окружения

Вы можете установить переменные окружения в файле `.env`:

```bash
# .env файл
TEST_ENV=dev
PYTEST_ARGS=-v --tb=short
```

## 🐳 Docker Compose сервисы

### Основные сервисы

#### `samokat-tests`
Базовый сервис для запуска тестов
```bash
docker-compose run --rm samokat-tests
```

#### `samokat-smoke`
Быстрые критические тесты
```bash
docker-compose run --rm samokat-smoke
```

#### `samokat-regression`
Полные регрессионные тесты
```bash
docker-compose run --rm samokat-regression
```

#### `samokat-parallel`
Параллельный запуск тестов (требует больше ресурсов)
```bash
docker-compose run --rm samokat-parallel
```

### Сервис отчетов

#### `allure-serve`
Веб-сервер для просмотра Allure отчетов
```bash
# Запуск Allure сервера
docker-compose --profile allure up -d allure-serve

# Открыть в браузере: http://localhost:5050
```

## 📁 Структура volumes

Docker контейнер монтирует следующие директории:

```
./allure-results   -> /app/allure-results   # Результаты тестов для Allure
./allure-reports   -> /app/allure-reports   # Сгенерированные отчеты
./screenshots      -> /app/screenshots      # Скриншоты при ошибках
```

## 🔧 Настройка ресурсов

### Ограничения памяти и CPU

| Сервис | Память (лимит) | CPU (лимит) | Рекомендация |
|--------|----------------|-------------|--------------|
| `samokat-tests` | 2GB | 1.0 | Стандартные тесты |
| `samokat-parallel` | 4GB | 2.0 | Параллельные тесты |
| `allure-serve` | 512MB | 0.5 | Просмотр отчетов |

### Настройка в docker-compose.yml

```yaml
deploy:
  resources:
    limits:
      memory: 2G
      cpus: '1.0'
    reservations:
      memory: 512M
      cpus: '0.5'
```

## 🚀 Примеры использования

### Разработка
```bash
# Запуск smoke тестов для быстрой проверки
./run-docker-tests.sh smoke

# Запуск конкретного теста
./run-docker-tests.sh smoke --args='-k test_order_buttons'

# Отладка в контейнере
./run-docker-tests.sh shell
```

### CI/CD
```bash
# Сборка и smoke тесты
./run-docker-tests.sh build
./run-docker-tests.sh smoke --env=stage

# Полное тестирование
./run-docker-tests.sh regression --env=stage
```

### Просмотр результатов
```bash
# Запуск Allure сервера
./run-docker-tests.sh allure

# Просмотр логов
./run-docker-tests.sh logs
```

## 🐛 Отладка и решение проблем

### Проблемы со сборкой

#### Ошибка установки браузеров
```bash
# Очистка и пересборка
./run-docker-tests.sh clean
./run-docker-tests.sh build
```

#### Недостаток места на диске
```bash
# Очистка Docker системы
docker system prune -a --volumes
```

### Проблемы с запуском тестов

#### Браузер не запускается
```bash
# Проверка в контейнере
./run-docker-tests.sh shell
playwright install --dry-run
```

#### Тесты падают с timeout
```bash
# Увеличение timeout для медленных окружений
./run-docker-tests.sh smoke --args='--timeout=60'
```

### Мониторинг ресурсов

```bash
# Просмотр использования ресурсов
docker stats

# Логи контейнера в реальном времени
docker-compose logs -f samokat-tests
```

## 📊 Производительность

### Время выполнения (примерное)

| Тип тестов | Время | Параллельно | Описание |
|------------|-------|-------------|----------|
| Smoke | ~10 сек | ~5 сек | Критические тесты |
| Regression | ~30 мин | ~15 мин | Полные тесты |
| Full | ~45 мин | ~20 мин | Все тесты |

### Рекомендации по оптимизации

1. **Используйте smoke тесты** для быстрой проверки
2. **Параллельный запуск** для экономии времени
3. **Фильтрация тестов** по маркерам или имени
4. **Кеширование образов** для ускорения сборки

## 🔒 Безопасность

### Пользователь в контейнере
```dockerfile
# Непривилегированный пользователь
RUN useradd -m -u 1001 testuser
USER testuser
```

### Ограничения доступа
- Контейнер запускается от непривилегированного пользователя
- Нет доступа к host networking
- Ограниченные ресурсы CPU и памяти

## 🚀 Интеграция с CI/CD

### GitHub Actions
```yaml
- name: Run Docker Tests
  run: |
    ./run-docker-tests.sh build
    ./run-docker-tests.sh smoke --env=stage
```

### GitLab CI
```yaml
test:
  script:
    - ./run-docker-tests.sh build
    - ./run-docker-tests.sh regression
```

## 📝 Обслуживание

### Регулярные задачи

```bash
# Обновление образа (еженедельно)
./run-docker-tests.sh clean
./run-docker-tests.sh build

# Очистка старых данных
docker system prune --volumes
```

### Мониторинг

```bash
# Размер образов
docker images

# Использование места
docker system df
```

---

## 🤝 Поддержка

При возникновении проблем:

1. Проверьте логи: `./run-docker-tests.sh logs`
2. Войдите в контейнер: `./run-docker-tests.sh shell`
3. Очистите и пересоберите: `./run-docker-tests.sh clean && ./run-docker-tests.sh build`

Made with ❤️ for Docker containerized testing
