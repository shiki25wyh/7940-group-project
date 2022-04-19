FROM python
COPY chatbot.py /
COPY requirements.txt /
RUN pip install pip update
RUN pip install -r requirements.txt
RUN pip install python-telegram-bot --upgrade


CMD ["python","chatbot.py"]