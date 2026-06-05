# StatusBoard App

Дашборд мониторинга статусов сервисов. Показывает состояние компонентов системы в реальном времени.
Приложение намеренно простое — весь смысл проекта в инфраструктуре вокруг него.

## Стек

- API: Python FastAPI с Prometheus метриками
- Frontend: Nginx + HTML/CSS/JS
- БД: PostgreSQL через Yandex Managed PostgreSQL
- Registry: Yandex Container Registry
- CI/CD: GitHub Actions

## Структура

    api/
    ├── main.py           — FastAPI с эндпоинтами /health, /services, /metrics
    ├── requirements.txt
    ├── Dockerfile        — multi-stage build, запуск от non-root пользователя
    └── tests/
        └── test_api.py
    frontend/
    ├── index.html        — дашборд статусов
    ├── nginx.conf        — конфиг с proxy_pass на API
    └── Dockerfile
    docker-compose.yaml
    .github/workflows/
    ├── ci.yaml
    └── cd.yaml

## Локальная разработка

Для быстрой проверки изменений без деплоя в кластер — docker-compose поднимает API, Frontend и локальный PostgreSQL одной командой:

    docker-compose up

- Приложение: http://localhost
- API: http://localhost:8000/api/services
- Health: http://localhost:8000/api/health

Остановить: docker-compose down

## CI/CD

При каждом коммите в main:
1. Тесты (pytest)
2. Сканирование Docker образов (Trivy)
3. Сборка образов
4. Push в Yandex Container Registry

При создании тега v*:

    git tag v1.0.0
    git push origin v1.0.0

1. Сборка образов с тегом версии
2. Push в registry
3. Деплой в Kubernetes
4. Проверка rollout

## Секреты репозитория

- YC_SA_KEY — JSON ключ сервисного аккаунта в base64
- YC_REGISTRY_ID — ID Yandex Container Registry
- KUBE_CONFIG — kubeconfig в base64
