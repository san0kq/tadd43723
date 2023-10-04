# Инструкция по развертыванию проекта

Этот README предоставляет пошаговую инструкцию по установке и настройке проетка tadd43723 на сервере.

## Шаг 1: Установка необходимых компонентов

Установите следующие пакеты на сервере:

- Python 3.10
- python3-pip
- python3-dev
- libpq-dev
- PostgreSQL и PostgreSQL-contrib
- Nginx
- Poetry

## Шаг 2: Создание базы данных PostgreSQL

Создайте базу данных PostgreSQL, которая будет использоваться проектом.

## Шаг 3: Клонирование проекта на сервер

Склонируйте проект на сервер.

## Шаг 4: Установка зависимостей проекта

Установите Poetry как пакетный менеджер в проекте:
<pre>
```bash
poetry init
</pre>

Затем выполните следующую команду для установки зависимостей проекта:
<pre>
```bash
poetry install
</pre>

## Шаг 5: Активация виртуального окружения и установка Gunicorn
Убедитесь, что виртуальное окружение активировано:
<pre>
```bash
poetry shell
poetry add gunicorn
</pre>

## Шаг 6: Настройка файлов проекта
В файле settings.py вашего проекта установите нужные IP-адреса или доменные имена в переменной ALLOWED_HOSTS, включая "localhost".

## Шаг 7: Конфигурация .env файла
В файле конфигурации проекта .env установите необходимые значения для работы базы данных и проекта.

## Шаг 8: Выполнение миграции
Выполните миграцию для создания необходимых таблиц:
<pre>
```bash
python3 manage.py migrate
</pre>

## Шаг 9: Создание файла сокета для Gunicorn
Создайте файл сокета для Gunicorn:
<pre>
```bash
sudo nano /etc/systemd/system/gunicorn.socket
</pre>
Содержимое файла:

<pre>
```gunicorn.socket
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
</pre>

## Шаг 10: Создание служебного файла systemd для Gunicorn
Создайте служебный файл systemd для Gunicorn:
<pre>
```bash
sudo nano /etc/systemd/system/gunicorn.service
</pre>
Содержимое файла:
<pre>
```gunicorn.service
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=user_name # имя юзера для запуска
Group=www-data
WorkingDirectory=/home/user_name/tadd43723
ExecStart=*здесь указывается путь к виртуальному окружению проекта* \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          tadd43723.wsgi:application

[Install]
WantedBy=multi-user.target
</pre>

## Шаг 11: Запуск и активация сокета Gunicorn
Запустите и активируйте сокет Gunicorn:
<pre>
```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
</pre>

## Шаг 12: Создание и настройка серверного блока Nginx
Создайте и настройте серверный блок Nginx:
<pre>
```bash
sudo nano /etc/nginx/sites-available/tadd43723
</pre>
Содержимое файла:
<pre>
```tadd43723
server {
    listen 80;
    server_name *IP-адрес сервера или доменное имя*;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/user_name/tadd43723;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
</pre>

## Шаг 13: Активация файла Nginx
Активируйте файл серверного блока Nginx:
<pre>
```bash
sudo ln -s /etc/nginx/sites-available/tadd43723 /etc/nginx/sites-enabled
</pre>

## Шаг 14: Перезапуск Nginx
Перезапустите Nginx:
<pre>
```bash
sudo systemctl restart nginx
</pre>

## Шаг 15: Настройка брандмауэра
Разрешите трафик для Nginx:
<pre>
```bash
sudo ufw allow 'Nginx Full'
```
</pre>
Теперь проект должен быть развернут и доступен на сервере.