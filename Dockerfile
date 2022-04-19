FROM python
COPY chatbot.py /
COPY requirements.txt /
RUN pip install pip update
RUN pip install -r requirements.txt
RUN pip install python-telegram-bot --upgrade

ARG ACCESS_TOKEN
ARG HOST
ARG PASSWORD
ARG REDISPORT

ENV ACCESS_TOKEN=$ACCESS_TOKEN
ENV HOST=$HOST
ENV PASSWORD=$PASSWORD
ENV REDISPORT=$REDISPORT

CMD ["python","chatbot.py"]