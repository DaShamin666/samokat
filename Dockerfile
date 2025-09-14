# Используем официальный образ Playwright
FROM mcr.microsoft.com/playwright:v1.55.0-noble

# Устанавливаем Python и pip (если не установлены)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# Создаем директории для отчетов и артефактов
RUN mkdir -p /app/allure-results /app/allure-reports /app/screenshots

# Копируем исходный код проекта
COPY . .

# Настраиваем права для существующего пользователя pwuser
RUN chown -R pwuser:pwuser /app
USER pwuser

# Устанавливаем рабочую директорию для пользователя
WORKDIR /app

# Указываем команду по умолчанию
CMD ["python3", "-m", "pytest", "-m", "smoke", "-v"]
