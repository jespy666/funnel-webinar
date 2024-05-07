# Воронка вебинар
### Описание
___

Воронка продаж с помощью Юзербота (Pyrogram)
## Схема воронки
|     Время      | Текст  |                   Точка отсчета                   |  Триггеры  |
|:--------------:|:------:|:-------------------------------------------------:|:----------:|
|    6 минут     | Текст1 |                 Первое сообщение                  |            |
|    39 минут    | Текст2 |               Время отправки Текст1               |  триггер1  |
| 1 день  2 часа | Текст3 | Время отправки Текст2 или Время триггера Триггер1 |  |
## Стэк
___
![Static Badge](https://img.shields.io/badge/Pyrogram-2.0.106-orange)  
![Static Badge](https://img.shields.io/badge/SQLAlchemy-2.0.29-red)  
![Static Badge](https://img.shields.io/badge/Alembic-1.13.1-blue)

## Установка 
___
1. Клонировать репозиторий  
    - `git clone` https://github.com/jespy666/funnel-webinar.git
2. Устновить зависимости
    - `pip install -r requirements.txt`
3. Сделать миграции
   - `make migrations`
   - `make migrate`
4. Запустить скрипт
    - `make run`