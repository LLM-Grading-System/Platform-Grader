# Воркер для проверки

## Разработка

### Переменные окружения

```env
# Application
MODE=dev
# Mistral
MISTRAL_API_KEY=api-key
MISTRAL_MODEL=codestral-latest
## Minio Envs
MINIO_PORT=9000
MINIO_HOST=localhost
MINIO_ROOT_USER=minio
MINIO_ROOT_PASSWORD=password
MINIO_ACCESS_KEY=3uGgBDZL6on2taEBZeBO
MINIO_SECRET_KEY=R0JGpfea5RXqe6xIvptcUuvbxd2t7QsOYqk0StBO
MINIO_BUCKET=submissions
# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:29092
KAFKA_UI_ADMIN_LOGIN=admin
KAFKA_UI_ADMIN_PASSWORD=password
# Backend
API_HOST=localhost
API_PORT=5000
```

### Запуск

```bash
uv run python -m src.app
```
