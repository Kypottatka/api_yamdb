
# API Yatube
API проекта **Yatube**. Позволяет **регистрировать** нового пользователя, **размещать**, **удалять** или **редактировать** от его имени посты и комментарии, а также **подписываться** на других пользователей.  

Возможен просмотр доступных на проекте групп, постов и комментариев к ним. Также для авторизованного пользователя реализована возможность просмотра его уже существующих подписок.

## Технологии

* Python 3.7
* Django 3.2
* DRF 3.12
* Simple JWT 4.7.2
* Djoser

## Запуск проекта

* Cоздать и активировать виртуальное окружение:

`python3 -m venv env`   
`source env/bin/activate`

* Установить зависимости из файла requirements.txt:

`python3 -m pip install --upgrade pip`
`pip install -r requirements.txt`

* Выполнить миграции:

`python3 manage.py migrate`

* Запустить проект:

`python3 manage.py runserver`

## Доступ
Возможен анонимный доступ в режиме `read-only` ко всем эндпоинтам, кроме эндпоинта `follow/`.

## Авторизация
* Пример `POST`-запроса для **создания аккаунта** к эндпоинту `users/` 

  ```
  {  
      "username": "your_username",  
      "password": "your_password"  
  }
  ```
* Пример `POST`-запроса для **получения токена** к эндпоинту `jwt/create/` 

  ```
  {  
      "username": "your_username",  
      "password": "your_password"  
  }
  ```
--
Автор: Евгения Рыжих  / [tg.me/zyrgve](https://telegram.me/zyrgve)
 

