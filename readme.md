# Team Finder

Team Finder - Сервис для поиска соавторов и организации командной работы над некоммерческими проектами.

## Возможности

- просмотр активных проектов с фильтрацией;
- авторизация через email и пароль;
- просмотр профилей участников;
- настройка личной информации;
- управление собственными проектами (создание, корректировка);
- сохранение понравившихся проектов в избранное;
- запрос на вступление в команду;
- поиск пользователей с сортировкой (варианту 1);

## Стек

- Python 3.9
- Django 3.2
- DRF (Django REST Framework)
- PostgreSQL 16
- Docker Compose
- Pillow
- python-decouple

## Страницы интерфейса

Пользовательская часть построена на шаблонах Django:

- / и /projects/list/ - список проектов;
- /users/register/ - регистрация;
- /users/login/ - вход;
- /users/<id>/ - просмотр профиля;
- /users/edit-profile/ - редактирование профиля;
- /users/change-password/ - обновление пароля;
- /users/list/ - каталог пользователей;
- /projects/<id>/ - страница проекта;
- /projects/create-project/ - создание нового проекта;
- /projects/<id>/edit/ - редактирование проекта;
- /projects/favorites/ - список избранных проектов.

### API

REST API доступен по маршруту `/api/v1/`.  
Документация (Swagger UI) — `/api/v1/docs/`.  
Схема в формате OpenAPI — `/api/v1/schema/`.

#### Основные эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/v1/projects/` | Список проектов |
| POST | `/api/v1/projects/` | Создать проект |
| GET | `/api/v1/projects/{id}/` | Детали проекта |
| PUT/PATCH | `/api/v1/projects/{id}/` | Обновить проект |
| DELETE | `/api/v1/projects/{id}/` | Удалить проект |
| GET | `/api/v1/users/` | Список пользователей |
| GET | `/api/v1/users/{id}/` | Профиль пользователя |
| POST | `/api/v1/token/` | Получить JWT-токен |
| POST | `/api/v1/token/refresh/` | Обновить JWT-токен |

Пример ответа для `GET /api/v1/projects/`:

```json
{
  "count": 12,
  "next": "http://127.0.0.1:8000/api/v1/projects/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Название проекта",
      "description": "Описание проекта",
      "github": "https://github.com/user/repo",
      "status": "open",
      "pub_date": "2026-06-06T12:00:00Z",
      "updated_at": "2026-06-06T12:00:00Z",
      "author": 1,
      "participants": []
    }
  ]
}
```

## Настройка окружения

Скопируйте .env_example в .env и укажите свои значения.

Пример:

DJANGO_SECRET_KEY=change_for_safety
DJANGO_DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

POSTGRES_DB=team_finder_1var
POSTGRES_USER=team_finder_1var
POSTGRES_PASSWORD=team_finder_1var
POSTGRES_HOST=db
POSTGRES_PORT=5432

Для локального запуска без Docker в POSTGRES_HOST нужно указать localhost, а в POSTGRES_PORT - порт локальной базы.

## Запуск через Docker Compose

1. Создайте файл .env на основе .env_example.

2. Запустите сборку:

docker compose up --build -d

3. Выполните миграции:

docker compose exec web python manage.py migrate

4. Создайте администратора:

docker compose exec web python manage.py createsuperuser

5. Откройте проект:

- сайт: http://127.0.0.1:8000/
- админка: http://127.0.0.1:8000/admin/

## Локальный запуск без Docker

1. Установите зависимости:

pip install -r requirements.txt

2. Настройте PostgreSQL и укажите параметры в .env.

3. Примените миграции:

python manage.py migrate

4. Запустите сервер:

python manage.py runserver

## Для ревьюера

- шаблонная часть реализована через Django views и templates;
- проект использует PostgreSQL в качестве СУБД;
- конфиденциальные данные внесены в .env;
- загруженные файлы сохраняются в media/;
- данные PostgreSQL в Docker сохраняются в volume postgres_data.

