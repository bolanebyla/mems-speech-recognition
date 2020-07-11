FROM python:3.7

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/


COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN sudo apt install libsndfile
RUN sudo apt install ffmpeg

EXPOSE 8080

RUN chmod a+x ./run.sh

ENTRYPOINT ["./run.sh"]