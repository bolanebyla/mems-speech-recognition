
# mems-speech-recognition
Чат бот и web-приложение с использованием нейронной сети для обработки двух голосовых команд: "Грусть" и "Мем". 

## Стек разработки
Python 3.7

Nginx + Gunicorn + Flask

Нейросеть: keras

## Установка ffmpeg
- для windows: вставить файл ffmpeg.exe в папку с проектом (скачать сборку ffmpeg
можно по [ссылке](https://ffmpeg.zeranoe.com/builds/), ffmpeg.exe внутри bin)
- для linux: `$ sudo apt-get install ffmpeg`

## Конфигурация nginx

    server {
        listen 80;
        server_name host_name.com;
        
        # Static files location
        location ^~/static/ {
           root /var/www/mems-speech-recognition/;
           error_page 404 = 404;
        }
        location / {
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_pass http://127.0.0.1:8080;
        }
    }



## Установка и настройка Let's Encrypt
    $ sudo apt install python-certbot-nginx
    $ sudo certbot --nginx -d host_name.com

## Запуск проекта 
    ./run.sh
