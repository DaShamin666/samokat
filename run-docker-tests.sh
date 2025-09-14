#!/bin/bash

# Скрипт для запуска тестов Samokat в Docker

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода помощи
show_help() {
    echo -e "${BLUE}🛴 Samokat Docker Test Runner${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""
    echo "Использование: $0 [КОМАНДА] [ОПЦИИ]"
    echo ""
    echo -e "${YELLOW}Команды:${NC}"
    echo "  build              Собрать Docker образ"
    echo "  smoke              Запустить smoke тесты (быстрые критические тесты)"
    echo "  regression         Запустить regression тесты (полные тесты)"
    echo "  full               Запустить все тесты"
    echo "  parallel           Запустить тесты в параллельном режиме"
    echo "  allure             Запустить Allure сервер для просмотра отчетов"
    echo "  clean              Очистить контейнеры и образы"
    echo "  logs               Показать логи контейнера"
    echo "  shell              Войти в контейнер для отладки"
    echo ""
    echo -e "${YELLOW}Опции:${NC}"
    echo "  --env=[dev|stage]  Окружение для тестов (по умолчанию: dev)"
    echo "  --args='...'       Дополнительные аргументы для pytest"
    echo "  --rebuild          Пересобрать образ перед запуском"
    echo "  --help             Показать эту справку"
    echo ""
    echo -e "${YELLOW}Примеры:${NC}"
    echo "  $0 smoke                           # Запустить smoke тесты"
    echo "  $0 regression --env=stage          # Regression тесты на stage"
    echo "  $0 full --args='-k test_order'     # Все тесты с фильтром"
    echo "  $0 parallel --rebuild              # Параллельные тесты с пересборкой"
    echo ""
}

# Функция для логирования
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ОШИБКА]${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[ПРЕДУПРЕЖДЕНИЕ]${NC} $1"
}

# Парсинг аргументов
COMMAND=""
TEST_ENV="dev"
PYTEST_ARGS=""
REBUILD=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --env=*)
            TEST_ENV="${1#*=}"
            shift
            ;;
        --args=*)
            PYTEST_ARGS="${1#*=}"
            shift
            ;;
        --rebuild)
            REBUILD=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            if [[ -z "$COMMAND" ]]; then
                COMMAND="$1"
            else
                error "Неизвестный аргумент: $1"
                show_help
                exit 1
            fi
            shift
            ;;
    esac
done

# Если команда не указана, показываем справку
if [[ -z "$COMMAND" ]]; then
    show_help
    exit 1
fi

# Экспорт переменных окружения для docker-compose
export TEST_ENV="$TEST_ENV"
export PYTEST_ARGS="$PYTEST_ARGS"

# Функция для сборки образа
build_image() {
    log "Сборка Docker образа..."
    docker-compose build samokat-tests
    log "✅ Образ успешно собран"
}

# Функция для очистки
clean_containers() {
    log "Очистка Docker контейнеров и образов..."
    docker-compose down --rmi all --volumes --remove-orphans 2>/dev/null || true
    docker system prune -f
    log "✅ Очистка завершена"
}

# Функция для просмотра логов
show_logs() {
    log "Показ логов последнего запуска..."
    docker-compose logs samokat-tests
}

# Функция для входа в контейнер
enter_shell() {
    log "Вход в контейнер для отладки..."
    docker-compose run --rm samokat-tests /bin/bash
}

# Функция для запуска Allure сервера
start_allure() {
    log "Запуск Allure сервера..."
    docker-compose --profile allure up -d allure-serve
    log "✅ Allure сервер запущен на http://localhost:5050"
    log "Для остановки выполните: docker-compose --profile allure down"
}

# Основная логика команд
case $COMMAND in
    build)
        build_image
        ;;
    
    smoke)
        log "🔥 Запуск smoke тестов (окружение: $TEST_ENV)"
        if [[ "$REBUILD" == "true" ]]; then
            build_image
        fi
        docker-compose run --rm samokat-smoke
        ;;
    
    regression)
        log "🔄 Запуск regression тестов (окружение: $TEST_ENV)"
        if [[ "$REBUILD" == "true" ]]; then
            build_image
        fi
        docker-compose run --rm samokat-regression
        ;;
    
    full)
        log "🎯 Запуск всех тестов (окружение: $TEST_ENV)"
        if [[ "$REBUILD" == "true" ]]; then
            build_image
        fi
        docker-compose run --rm samokat-full
        ;;
    
    parallel)
        log "🚀 Запуск тестов в параллельном режиме (окружение: $TEST_ENV)"
        if [[ "$REBUILD" == "true" ]]; then
            build_image
        fi
        docker-compose run --rm samokat-parallel
        ;;
    
    allure)
        start_allure
        ;;
    
    clean)
        clean_containers
        ;;
    
    logs)
        show_logs
        ;;
    
    shell)
        enter_shell
        ;;
    
    *)
        error "Неизвестная команда: $COMMAND"
        show_help
        exit 1
        ;;
esac

