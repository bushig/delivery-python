# Демо проект к курсу "Domain Driven Design и Clean Architecture на языке Java"
📚 Подробнее о курсе: [microarch.ru/courses/ddd/languages/java](https://microarch.ru/courses/ddd/languages/java?utm_source=gitlab&utm_medium=repository)

---

## Миграции БД (Alembic)

```bash
# Применить все миграции
uv run alembic upgrade head

# Создать новую миграцию (автогенерация по изменениям моделей)
uv run alembic revision --autogenerate -m "description"

Перед запуском убедитесь, что переменные окружения настроены (см. `.env.example`). URL подключения можно переопределить через `sqlalchemy.url` в `alembic.ini` или через переменную окружения.

---

## Условия использования

Вы можете использовать и модифицировать данный код **в образовательных целях**, при условии сохранения ссылки на курс и оригинального источника.

---

# Запросы к БД
```
SELECT * public.assignments;
SELECT * FROM public.couriers;
SELECT * FROM public.orders;
SELECT * public.outbox;
```

# Очистка БД (все кроме справочников)
```
DELETE FROM public.assignments;
DELETE FROM public.couriers;
DELETE FROM public.orders;

DELETE FROM public.outbox;
```

# Генерация моделей из OpenAPI

Pydantic-модели генерируются автоматически из `openapi_contract.yaml` с помощью `fastapi-code-generator`.

Сами роутеры не генеририруются на этом этапе так как в fastapi из коробки нет поддержки class based views и для этого нужно искать другие библиотеки (чтобы отдельной был интерфейс и отдельно сам класс).

## Быстрая генерация

```bash
./scripts/generate_http.sh
```

## Что генерируется

- `src/adapters/in_/http/models.py` — Pydantic-модели для запросов/ответов

## Когда перегенерировать

Запускайте генерацию после каждого изменения `openapi_contract.yaml`:
- Добавили новый endpoint
- Изменили схему запроса/ответа
- Добавили новый тег операции

# Генерация gRPC клиента из Protobuf
```
mvn clean compile
```
# Генерация интеграционных событий Kafka из Protobuf
```
mvn clean compile
```

## Лицензия

Код распространяется под лицензией [MIT](./LICENSE).  
© 2025 microarch.ru