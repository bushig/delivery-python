# Демо проект к курсу "Domain Driven Design и Clean Architecture на языке Java"
📚 Подробнее о курсе: [microarch.ru/courses/ddd/languages/java](https://microarch.ru/courses/ddd/languages/java?utm_source=gitlab&utm_medium=repository)

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

# Генерация HTTP-роутеров и моделей из OpenAPI

HTTP-роутеры и Pydantic-модели генерируются автоматически из `openapi_contract.yaml` с помощью `fastapi-code-generator`.

## Быстрая генерация

```bash
./scripts/generate_http.sh
```

## Что генерируется

- `src/adapters/in_/http/models.py` — Pydantic-модели для запросов/ответов
- `src/adapters/in_/http/routers/*.py` — роутеры по тегам OpenAPI (CreateOrder, CompleteOrder, и т.д.)
- `src/adapters/in_/http/main.py` — агрегатор всех роутеров

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