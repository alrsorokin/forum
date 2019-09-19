# Forum API

## Запуск проекта

* Собрать проект 
```sh
make build
```

* Запустить проект
```sh
make start
```
* Проект будет доступен по адресу http://localhost:5000/

## Описание API
=============================================
* Получить список разделов
```sh
Method: GET
http://localhost:5000/api/v1/sections
```
* Добавить раздел
```sh
Method: POST
http://localhost:5000/api/v1/sections
data = {
    'theme': 'Тема',
    'description': 'Описание',
}
```

* Получить информацию по разделу
```sh
Method: GET
http://localhost:5000/api/v1/sections/<id раздела>
```

* Удалить раздел
```sh
Method: DELETE
http://localhost:5000/api/v1/sections/<id раздела>
```
* Изменить раздел
```sh
Method: PUT
http://localhost:5000/api/v1/sections/<id раздела>
data = {
    'theme': 'Новая тема',
    'description': 'Новое описание',
}
```
=============================================
* Получить список постов в разделе
```sh
Method: GET
http://localhost:5000/api/v1/sections/<id раздела>/posts
```
* Добавить пост в раздел
```sh
Method: POST
http://localhost:5000/api/v1/sections/<id раздела>/posts
data = {
    'theme': 'Тема поста',
    'description': 'Описание описание',
}
```

* Получить информацию по посту со всеми комментариями
```sh
Method: GET
http://localhost:5000/api/v1/sections/<id раздела>/posts/<id поста>
```

* Удалить пост
```sh
Method: DELETE
http://localhost:5000/api/v1/sections/<id раздела>/posts/<id поста>
```
* Изменить пост
```sh
Method: PUT
http://localhost:5000/api/v1/sections/<id раздела>/posts/<id поста>
data = {
    'theme': 'Новая тема поста',
    'description': 'Новое описание поста',
}
```
=============================================
* Добавить комментарий к посту
```sh
Method: POST
http://localhost:5000/api/v1/sections/<id раздела>/posts/<id поста>/comments
data = {
    'text': 'Текст комментария',
}
```

## Доступные команды из Makefile
* Собрать проект 
```sh
make build
```
* Запустить проект
```sh
make start
```
* Остановить все контейнеры
```sh
make stop
```
* Запуск тестов
```sh
make test
```
