# StatusBoard App

Тестовое приложение для дипломного проекта. Дашборд мониторинга статусов сервисов.

## Стек

- API: Python FastAPI + Prometheus метрики
- Frontend: Nginx + статический HTML
- БД: PostgreSQL (Yandex Managed)
- Registry: Yandex Container Registry
- CI/CD: GitHub Actions

## Структура

    api/              - FastAPI приложение
    frontend/         - Nginx + статика
    .github/workflows/
        ci.yaml       - Lint + Test + Build + Push при коммите в main
        cd.yaml       - Build + Push + Deploy при создании тега v*

## Локальная разработка

    docker-compose up

Приложение доступно на http://localhost

## CI/CD

CI - при каждом коммите в main:
1. Запуск тестов
2. Сборка Docker образов
3. Push в Yandex Container Registry

CD - при создании тега:

    git tag v1.0.0
    git push origin v1.0.0

1. Сборка образов с версионным тегом
2. Push в registry
3. Деплой в Kubernetes кластер

## Секреты репозитория

- YC_SA_KEY - Ключ сервисного аккаунта в base64
- KUBE_CONFIG - kubeconfig в base64
