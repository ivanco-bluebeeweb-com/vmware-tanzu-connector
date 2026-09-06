# VMware Tanzu Connector — Discovery & Vendor API Specification

**Официальный сайт:** https://tanzu.vmware.com  
**Базовый эндпоинт API:** `https://<tanzu-mission-control-api>/v1alpha1`  
**Схема авторизации:** VMware Cloud Services API Token (CSP Refresh Token)

## Поддерживаемые сущности API
- кластеры (/v1alpha1/clusters)
- неймспейсы (/v1alpha1/namespaces)
- политики политик (/v1alpha1/policies)
- инспекции аудита

## Архитектурные требования
- Использование безопасного клиента с контролем таймаутов, повторных попыток (backoff) и обработкой rate limit.
- Валидация входных данных через Pydantic-схемы без утечки чувствительных полей в логи.
- Тестовая точка проверки подключения: `GET /v1alpha1/clusters`.
