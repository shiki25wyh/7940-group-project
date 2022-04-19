FROM python
COPY chatbot.py /
COPY requirements.txt /
RUN pip install pip update
RUN pip install -r requirements.txt
RUN pip install python-telegram-bot --upgrade

ENV ACCESS_TOKEN=5299443530:AAGzHEzIxWn3OGRqHJUgPQlyMhuzrkN4Q4w
ENV HOST=redis-11170.c8.us-east-1-3.ec2.cloud.redislabs.com
ENV PASSWORD=dZleUg0YWWO1a1zSBGoTGfQrf6tm1vnQ
ENV REDISPORT=11170

CMD ["python","chatbot.py"]