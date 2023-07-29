# Простой сервис для укорачивания ссылок.
Одностраничный сайт для генерации коротких ссылкок и переадрессации при переходе по ним.

## Инструкция по запуску
Для запуска произведите действия ниже.
Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

В корне проекта создайте .env файл.
Формат .env файла:

```
FLASK_APP=yacut
FLASK_ENV=production
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=MY SECRET KEY
```

## Об авторе
Разработано:
[Илья Савинкин](https://www.linkedin.com/in/ilya-savinkin-6002a711/)
