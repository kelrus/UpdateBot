FROM python:3.9

RUN mkdir -p /usr/src/app/
RUN apt-get update && apt-get upgrade
RUN pip install --upgrade pip
RUN pip install aiogram && pip install apscheduler
WORKDIR /usr/src/app/

COPY . /usr/src/app/

CMD ["python3", "BotMain.py"]
