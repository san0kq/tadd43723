1. Установить на сервере python3.10, python3-pip, postgresql, postgresql-contrib, nginx, poetry.
2. Создать базу данных PostgreSQL.
3. Склонировать проект на сервер.
4. Установить Poetry как пакетный менеджер в проекте и выполнить "poetry install" для установки зависимостей.
5. Убедиться, что виртуальное окружение активировано "poetry shell" и установить gunicorn "poetry add gunicorn".
6. В settings.py проекта установить нужные IP-адреса или доменные имена в переменной ALLOWED_HOSTS. Не забыть также
указать там "localhost".
7. В файле конфигураций проекта .env установить необходимые значения для работы базы данных и проекта.
8. Выполнить миграцию: 
python3 manage.py migrate

9. Создать файл сокета для Gunicorn.
sudo nano /etc/systemd/system/gunicorn.socket

Содержимое файла сокета:
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target

10. Создать служебный файл systemd для Gunicorn. 
sudo nano /etc/systemd/system/gunicorn.service

Содержимое файла:
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=user_name # имя юзера для запуска
Group=www-data
WorkingDirectory=/home/user_name/tadd43723
ExecStart=*здесь указывается пусть к виртуальному окружению проекта* \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          tadd43723.wsgi:application

[Install]
WantedBy=multi-user.target

11. Запуск и активация сокета Gunicorn.
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

12. Создать и открыть серверный блок Ngnix проекта:
sudo nano /etc/nginx/sites-available/tadd43723

Содержимое файла:
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

13. Активация файла:
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled

14. Перезапустить Nginx:
sudo systemctl restart nginx

15. Запустить команду:
sudo ufw allow 'Nginx Full'