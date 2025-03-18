<div id="header" align="center">
  <h1>Coiled Steel API</h1>
  <h2>Тестовое задание на стажировку IT HUB «Северстали»</h2>

  ![Python](https://img.shields.io/badge/-Python_3.10-000?&logo=Python)
  ![FastAPI](https://img.shields.io/badge/-FastAPI_0.115.11-000?&logo=FastAPI)
  ![Pydantic](https://img.shields.io/badge/-Pydantic_2.10.6-000?&logo=Pydantic)
  ![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy_2.0.39-000?&logo=SQLAlchemy)
  ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-000?&logo=PostgreSQL)
  ![Docker](https://img.shields.io/badge/-Docker-000?&logo=Docker)
  ![Pytest](https://img.shields.io/badge/-Pytest-000?&logo=Pytest)

</div>

Статус проверки линтеров и тестов:

[![coiled_steel_api_workflow](https://github.com/kaschenkkko/CoiledSteelAPI/actions/workflows/main.yaml/badge.svg)](https://github.com/kaschenkkko/CoiledSteelAPI/actions/workflows/main.yaml)

Документация к API доступна:

[API Documentation ](https://kaschenkkko.github.io/CoiledSteelAPI/)

<h2>Техническое задание проекта</h2>

### Обязательные пункты:

✅1. RESTFull API:
 - Добавление нового рулона на склад. Длина и вес — обязательные параметры. В случае успеха возвращает добавленный рулон
 - Удаление рулона с указанным id со склада. В случае успеха возвращает удалённый рулон
- Получение списка рулонов со склада. Рассмотреть возможность фильтрации по одному из диапазонов единовременно (id/веса/длины/даты добавления/даты удаления со склада)
- Получение статистики по рулонам за определённый период:
  - количество добавленных рулонов
  - количество удалённых рулонов
  - средняя длина, вес рулонов, находившихся на складе в этот период
  - максимальная и минимальная длина и вес рулонов находившихся на складе в этот период
  - суммарный вес рулонов на складе за период
  - максимальный и минимальный промежуток между добавлением и удалением рулона

✅2. Данные по рулонам должны храниться в базе данных (желательно PostgreSQL/SQLite)

✅3. Должны быть обработаны стандартные кейсы ошибок (например, недоступна БД, не существует рулон при какой-то работе с ним)

✅4. Используемый стек: FastAPI, SQLAlchemy, pydantic (версии и до 2.0, и после 2.0 подойдут)

### Бонусная часть:

✅1. Получение списка рулонов с фильтрацией работает по комбинации нескольких диапазонов сразу

❌2. Получение статистики по рулонам дополнительно возвращает:
- день, когда на складе находилось минимальное и максимальное количество рулонов за указанный период
- день, когда суммарный вес рулонов на складе был минимальным и максимальным в указанный период

✅3. Проект должен быть обёрнут в Docker

✅4. Конфигурации к подключению к БД должны быть настраиваемыми через файл или ENV

✅5. Проект должен быть покрыт тестами

✅6. Проект должен проходить mypy, flake8 и прочее

✅7. Отсутствие глобальных переменных

<details><summary><h2>Запуск проекта</h2></summary>

- Перейдите в папку **docker**.
- Создайте файл **.env** с переменными окружения:
    ```
    DB_HOST=
    DB_PORT=
    DB_NAME=
    POSTGRES_USER=
    POSTGRES_PASSWORD=

    TEST_DB_HOST=
    TEST_DB_PORT=
    TEST_DB_NAME=
    TEST_POSTGRES_USER=
    TEST_POSTGRES_PASSWORD=
    ```
- Запустите контейнеры:
  ```
  docker-compose up -d --build
  ```
- В контейнере **backend** выполните миграции:
  ```
  docker-compose exec backend alembic upgrade head
  ```
- Команда для запуска тестов:
  ```
  docker-compose exec backend pytest
  ```
</details>