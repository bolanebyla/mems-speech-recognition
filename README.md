
# mems-speech-recognition
Чат бот и web-приложение с использованием нейронной сети для обработки двух голосовых команд: "Грусть" и "Мем". 
[@mems_speech_recognition_bot](https://telegram.me/mems_speech_recognition_bot)
## Стек разработки
Python 3.7

Nginx + Gunicorn + Flask

Нейросеть: keras

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

## Запуск проекта с помощью docker (docker-compose)
1. Указать переменные окружения в файле `docker-compose.yaml`:
    - `TG_token` - токен бота в telegram
    - `HOST` - адрес сервера (пример: https://excample.com/)
 2. В директории проекта `$ docker-compose up ` 
(флаг `-d` - запуск в фоне)

## Запуск проекта без docker
1. Установка ffmpeg
    - для windows: вставить файл ffmpeg.exe в папку с проектом (скачать сборку ffmpeg
    можно по [ссылке](https://ffmpeg.zeranoe.com/builds/), ffmpeg.exe внутри bin)
    - для linux: `$ sudo apt-get install ffmpeg`
2. Установка libsndfile1 (linux) `$ apt-get install libsndfile1`
3. Установка библиотек `$ pip install -r requirements.txt`
3. Запуск проекта `./run.sh`

    
