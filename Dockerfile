# Используем официальный Python образ с Ubuntu base
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    # Зависимости для Playwright браузеров
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    # Дополнительные системные утилиты
    wget \
    curl \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libu2f-udev \
    libvulkan1 \
    xvfb \
    # Очистка кеша APT для уменьшения размера образа
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем Playwright браузеры
RUN playwright install --with-deps

# Копируем исходный код проекта
COPY . .

# Создаем директории для отчетов и артефактов
RUN mkdir -p /app/allure-results /app/allure-reports /app/screenshots

# Устанавливаем переменные окружения для Playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/root/.cache/ms-playwright

# Создаем скрипт для запуска тестов
COPY <<EOF /app/run_tests.sh
#!/bin/bash
set -e
echo "🛴 Запуск тестов Samokat в Docker контейнере"
echo "================================"
echo "Окружение: \${TEST_ENV:-dev}"
echo "Маркеры: \${TEST_MARKERS:-smoke}"
echo "Дополнительные параметры: \${PYTEST_ARGS}"
echo "================================"

# Формируем команду pytest
CMD="python -m pytest"

# Добавляем маркеры если указаны
if [ ! -z "\$TEST_MARKERS" ]; then
    CMD="\$CMD -m \$TEST_MARKERS"
fi

# Добавляем окружение если указано
if [ ! -z "\$TEST_ENV" ]; then
    CMD="\$CMD --env=\$TEST_ENV"
fi

# Добавляем дополнительные аргументы
if [ ! -z "\$PYTEST_ARGS" ]; then
    CMD="\$CMD \$PYTEST_ARGS"
fi

echo "Выполняем команду: \$CMD"
echo "================================"
eval \$CMD
EOF

RUN chmod +x /app/run_tests.sh

# Устанавливаем пользователя для безопасности
RUN useradd -m -u 1001 testuser && chown -R testuser:testuser /app
# Делаем директорию с браузерами доступной для всех пользователей
RUN chmod -R 755 /root/.cache/ms-playwright
USER testuser

# Указываем точку входа
ENTRYPOINT ["/app/run_tests.sh"]

# По умолчанию запускаем smoke тесты
CMD []
