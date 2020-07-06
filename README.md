# mems-speech-recognition

## Стэк разработки
nginx + gunicorn + flask

## Для работы проекта, нужен ffmpeg
Установка ffmpeg
    - для windows: вставить папку bin в папку с проектом
    - для linux: `sudo apt-get install ffmpeg`
## Конфигурация nginx

`server {`
    `listen 80;`
    `server_name host_name.com;`

    location /static/ {
       root your_path/mems-speech-recognition/static/;
    }


    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_pass http://127.0.0.1:8080;
    }`


## Настройка Let's Encrypt
    $ sudo apt install python-certbot-nginx
    $ sudo certbot --nginx -d host_name.com
