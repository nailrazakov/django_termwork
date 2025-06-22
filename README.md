# Название
Сервис управления рассылками.

## Используемые технологии
  * python
  * django
  * psycopg2
  * dotenv
  * ipython
  * Pillow

## Инструкция по развертыванию:
  * 
  * на основе файла .env.sample создать свой файл .env с настройками Джанго и Базы данных
  * фикстуры загружаются командами - python manage.py load_fixture и python manage.py load_blog_fixture
  * для создания суперпользователя использовать команду python manage.py csu  (admin@test.test - test(*password))
  * при запуске также будут также созданы пользователи без прав (visitor@test.test - test(*password)) 
  * и модератор с правами модератора (moderator@test.test - test(*password)) с правами удалить и публиковать
  * 
## Описание работы программы

## Автор проекта:
Разаков Наиль