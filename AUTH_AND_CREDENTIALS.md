# VMware Tanzu Connector — Auth & Credentials Standard

**Compliance:** AUTH_AND_CREDENTIALS_STANDARD.md (B1–B10)

## Схема аутентификации
- **Метод:** VMware Cloud Services API Token (CSP Refresh Token)
- **Хранение:** Секреты сохраняются изолированно в хранилище секретов платформы Imperal.
- **Валидация:** При сохранении ключа выполняется тестовый запрос `GET /v1alpha1/clusters`.
- **Отключение:** Удаление локальных ключей без воздействия на аккаунт вендора.
