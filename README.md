# Todo API

### Требования к системе

- python3

```bash
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10

```

- virtualenv

```bash
python3 -m pip install --user virtualenv
```

### Установка

В корневой директории выполнить:

```bash
virtualenv flask
flask/bin/pip install flask-httpauth
chmod a+x app.py
```

### Запуск

```bash
./app.py
```

### Api Documentation

#### Авторизация

Креды: user `miguel`, password `python`

Все ресурсы защищены BasicAuth

#### Модели

##### Task

```
{
  "uri": str,           // абсолютная ссылка на получение задачи
  "title": str,         // название задачи
  "description": str,   // описание задачи
  "done": bool          // маркер выполнения задачи
}
```

#### Ресурсы

##### Все задачи

URL: `http://localhost:5000/todo/api/v1.0/tasks`

Method: `GET`

Response:

```
{
  "tasks": [Task]
}
```

##### Добавление новой задачи

URL: `http://localhost:5000/todo/api/v1.0/tasks`

Method: `POST`

Data:

```
{
  "title": str,         // название задачи, обязательно, не пустая строка
  "description": str    // описание задачи, необязательно
}
```

Response:

```
{
  "task": Task  // добавленная задача
}
```

Errors:

`400` - Невалидные данные
