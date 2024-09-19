<h1>Запуск для локальной разработки</h1>

1. Создайте в корне проекта `.env` файл по аналогии с `.env-example`
2. Создайте и запустите контейнер с postgres
```commandline
docker-compose up -d
```
3. Создайте папку `versions` по пути `src/services/storage/migrations` 
4. Запустите первую миграцию
```commandline
alembic revision --autogenerate -m 'initial'
```
5. Проверьте корректность миграции и примените ее (модели таблиц лежат по пути `src/services/storage/schemas`)
```commandline
alembic upgrade head
```
