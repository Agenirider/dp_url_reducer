# Структура проекта 
- front - React SPA
- url_reducer - Django приложение
- proxy - nginx для сервировки статики Django в prod, а так же маршрутизации запросов к API
- redis - key-value хранилище для работы Celery и кеширования запросов
- reverse-proxy - обработка доменных имен и сортировка запросов

# Celery
Celery обслуживает задачи:
- удаление устаревших URL из БД

# Запуск проекта из PyCharm

1. Установить необходимое ПО
    1. Установить python 3
    2. Установить virtualenv
    3. Установить PyCharm


# Установка - Окружение
pip3 install -r requirements.txt

# Заполнение тестовыми данными 
создание админа
- python manage.py ensure_admin

создание списка доменов
- python manage.py ensure_domains

# Запуск проекта в тестовом режиме
* python manage.py runserver
* открыть папку front в IDE
* запустить npm i
* запустить npm start



# ENDPOINTS
1.admin/ - административная панель Django
2.url_reducer/ - API

# Работа с API (url_reducer/)
1. set_url
   + запрос POST 
   + body JSON {'url': 'xxxx', 'domain': 1, 'url': 'xxxxxxxx'}
   + domain - id домена из списка
   + url - адрес, указываемый пользователем вручную (по умолчанию - генерируется автоматически)
   + пример ответа {'res': 'url_created', 'url': 'dom123.com/vk_anton'}
                         ) 
   + доступные доменные имена:
       * domain1.link
       * dom123.com
       * test123.ru
       * lalala.we
       * blablabla.com

   + get_url/page=0> 
      * запрос GET 
      * пример ответа {'res': [{
                          'id': 1,
                          'domain': domain1.link,
                          'url': 'jsdlk',
                          'url_destination': 'www.ya.ru'}],
                         'prev_page': False,
                         'next_page': False}
      * пагинация обрабатывается автоматически
   
2. delete_url/1 - 
   + запрос DELETE
   + аргумент url_id
   + пример ответа - статус 200
   
3. redirect/domain/domain_subpart - 
  + запрос GET
  + reverse proxy переадресует на url_reducer на URL /url_reducer/redirect/domain/domain_subpart
  + находит в базе соответвие с внешним URL и переадресовывает на него

# Запуск задач для тестов
- celery -A partners worker -l INFO --pool=solo
- celery -A partners beat -l INFO

# Запуск в production mode
соотвествие доменных имен (для тестов)
- proxy - app.redirect.link
- front - api.redirect.link

  - запуск докера
  * docker-compose up -d --build





