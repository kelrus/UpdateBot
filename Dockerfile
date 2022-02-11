FROM python:3.9

RUN mkdir -p /usr/src/app/
RUN apt-get -y update && apt-get -y upgrade
RUN pip install --upgrade pip
RUN apt-get install sqlite3
RUN pip install aiogram && pip install apscheduler

WORKDIR /usr/src/app/

COPY . /usr/src/app/

CMD ["python3", "BotMain.py"]
