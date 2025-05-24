# 👥 Randomuser App (FastAPI + Jinja2)

Приложение на FastAPI для отображения пользователей, загружаемых с внешнего API. Реализованы:

- Пагинация с лимитом и смещением (limit / offset)
- Загрузка новых пользователей с внешнего API
- Отображение подробной информации о пользователе
- Показ случайного пользователя
- Юнит-тесты с моками

---

## 📦 Установка и запуск
##### В docker
Конфиги запуска из .env.default можно переопределить в .env.docker 

Если есть make 
```bash
# в корневой папке проекта
make all 
```
Если нет make
```bash
# в корневой папке проекта
docker compose -f docker_compose/all.yml -f docker_compose/db.yml --env-file env/.env.default --env-file env/.env.docker up --build -d  --force-recreate
```
можно заходить на http://localhost:8000/homepage

##### Локальный запуск
Конфиги запуска из .env.default можно пееропределить в .env.docker
```bash
uv sync
source .venv/bin/activate

# запушил env файлы чтобы было проще запустить
# запустить postgresql за пользователя postgres, сделать БД с название yadro_impulse_randomusers
# P.S. пользователя и название БД можно переименовать в env/.env
alembic upgrade head

python src/yadro_impulse_randomusers/main/web.py
```
можно заходить на http://localhost:8000/homepage
---

## 🚀 Стек технологий

- **FastAPI** — backend-фреймворк
- **Jinja2** — рендеринг HTML-шаблонов
- **SQLAlchemy 2.0 ORM** — работа с БД
- **PostgreSQL** — база данных
- **Alembic** — миграции
- **httpx + pytest** — тестирование
- **unittest.mock** — моки зависимостей

## 🧠 Обоснование выбора технологий

- **Веб-фреймворк: FastAPI**  
  Отлично подходит для того чтобы быстро создать маленький сайт с парой ручек. Есть поддержка Jinja2 ля создания фронтенда.

- **База данных: PostgreSQL**  
  Полностью совместима с SQLAlchemy ORM и активно используется в промышленной разработке. Open source


## 🤖 Генерация

Содержимое `README.md` было сгенерировано с использованием искусственного интеллекта (ChatGPT) и отредактирована вручную для точности и соответствия требованиям проекта.
