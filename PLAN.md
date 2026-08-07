# План: Исправление проблем проекта fastapi_app1

> Этот файл — единая точка контекста задачи. Обновляется по мере продвижения.
> Дублирует содержимое `/memories/session/plan.md` (память сессии) для видимости в проекте.

## 📌 Текущий статус (на 2026-08-07)
- [x] Проверка проекта завершена, отчёт выдан пользователю
- [x] План работ составлен и показан пользователю (ниже)
- [ ] Ответы на «Открытые вопросы» ещё не получены — НЕ начинать реализацию, пока пользователь не ответит на 3 вопроса (миграции / POST bookings / database.sql)
- Пользователь попросил сохранять этапы работы в файл для контекста будущих сессий

## ✅ Подтверждённые факты (проверено на 2026-08-06)
- Версии: pydantic 2.13.4, fastapi 0.139.0, sqlalchemy 2.0.51, alembic 1.18.5, Python 3.12
- `import main` успешен, но с `-W error::DeprecationWarning` падает: `PydanticDeprecatedSince20` из-за `class Config: orm_mode = True` в `app/schemas/hotels.py`
- `Base.metadata.tables` при импорте main = ТОЛЬКО `['bookings']` (остальные модели не импортируются; `app/models/__init__.py` пустой)
- `alembic heads` = `41501d76d81c`; цепочка: base → 713aac056ed6(hotels) → 3ac5813391de(пустая) → 63a4f4635e29(users) → 41501d76d81c(rooms+bookings)
- TestClient: GET /hotels/?filters → 200 (хардкод, фильтры игнорируются); GET /hotels/1 → 200; POST /hotels/bookings → **500 ResponseValidationError** (handler возвращает None при response_model=ShemaBooking)
- `.env` существует и валиден (иначе `settings = Setting()` упал бы на импорте)
- Репозиторий: git, ветка master, есть database.sql (seed-данные) и .env.example

---

Цель: устранить найденные при проверке проблемы (критичные + средние + ключевые косметические), выстроив работу «снизу вверх»: схемы → модели → миграции → сервисы → маршруты → верификация. Каждый этап логически опирается на предыдущий.

## Этап 0 — Подготовка
- 0.1 Проверить .env (все 5 переменных DB_*), доступность PostgreSQL
- 0.2 Зафиксировать исходное состояние: `alembic current`, есть ли данные в БД (чтобы не потерять при миграции)

## Этап 1 — Схемы (фундамент сериализации)
Файл: `app/schemas/hotels.py` (+ импорты в routers)
- 1.1 `class Config: orm_mode = True` → `model_config = ConfigDict(from_attributes=True)` (Pydantic v2)
- 1.2 Переименовать `ShemaBooking` → `SchemaBooking`, `ShemaHotel` → `SchemaHotel`
- 1.3 Исправить поле `starts` → `stars` (чтобы совпадало с query-параметром `stars`)
- 1.4 Обновить импорты в `app/routers/hotels.py` и `app/routers/bookings.py`

## Этап 2 — Модели (источник истины БД)
- 2.1 `app/models/__init__.py`: импортировать все модели (Hotels, Rooms, Users, Bookings) — чтобы регистрировались в `Base.metadata`
- 2.2 `app/models/bookings.py`: исправить Computed-выражения: `(date_from - date_to) * price` → `(date_to - date_from) * price`, `date_from - date_to` → `date_to - date_from`
- 2.3 `app/models/hotels.py`: `rooms_quanyity` → `rooms_quantity`
- 2.4 `app/models/users.py`: `email` + `unique=True`

## Этап 3 — Миграции (синхронизация схемы БД) — depends on Этап 2
- 3.1 Убедиться, что в `app/migrations/env.py` модели доступны (импорт `app.models`), чтобы autogenerate видел все таблицы
- 3.2 Решить стратегию: новая миграция поверх head ИЛИ squash всех 4 в одну чистую (рекомендация — squash, проект ранний)
- 3.3 Сгенерировать миграцию (`alembic revision --autogenerate`), вручную поправить rename колонки (`op.alter_column` вместо drop/add), если данные сохраняем
- 3.4 `alembic upgrade head`
- 3.5 Проверить `alembic current`/`history`, применить `database.sql` как seed при необходимости

## Этап 4 — Сервисный слой (бизнес-логика) — depends on Этап 2
- 4.1 `app/services/base.py`: `find_by_id` — вернуть сигнал об отсутствии (None → для 404)
- 4.2 Новый `app/services/hotels.py` с `HotelsService` (фильтрация по location/date/stars/has_spa)
- 4.3 `app/services/bookings.py` — использовать обновлённую модель, добавить метод создания брони

## Этап 5 — Маршруты (API) — depends on Этапы 1, 4
Файлы: `app/routers/hotels.py`, `app/routers/bookings.py`
- 5.1 `POST /hotels/bookings` — реализовать создание через сервис (или явная заглушка 501 с корректным ответом, но не `None` + response_model)
- 5.2 `GET /hotels/` — использовать параметры `location`, `date_from`, `date_to`, `stars`, `has_spa` (реальная фильтрация)
- 5.3 `GET /hotels/{hotel_id}` — аннотировать `date_from`/`date_to`, добавить 404
- 5.4 `GET /bookings/{booking_id}` — 404 при отсутствии
- 5.5 Проверить порядок маршрутов: `/bookings` не конфликтует с `/{hotel_id}`

## Этап 6 — Верификация — depends on все этапы
- 6.1 Импорт с `-W error::DeprecationWarning` (нет deprecation)
- 6.2 TestClient: все эндпоинты (GET /hotels/?filters, GET /hotels/1, POST /hotels/bookings, GET /bookings/, GET /bookings/1, 404-кейсы)
- 6.3 `alembic check` (или autogenerate --dry-run) — нет дрейфа схемы
- 6.4 Запуск `uvicorn main:app` + smoke-тест
- 6.5 Проверка данных: bookings.total_cost/total_days положительные, колонка rooms_quantity

## Решения/допущения
- Включено: критические (500 на POST, пустой models/__init__), средние (pydantic v2, computed, фильтры, 404), косметические опечатки (rooms_quanyity, Shema)
- Включено (обсуждается): наведение порядка в цепочке миграций
- Исключено: реальная авторизация/хэширование паролей, полный CRUD, Docker-окружение

## Открытые вопросы (уточнить до старта)
1. Стратегия миграций: squash в одну или новая поверх head? (рекомендую squash)
2. POST /hotels/bookings: реализовать полное создание записи или оставить заглушку, но с корректным 501?
3. Нужно ли обновлять `database.sql` (переименование rooms_quanyity)?
