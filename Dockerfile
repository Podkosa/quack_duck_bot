FROM python:3.10

WORKDIR /duck_bot
ENV TGBOT_API_TOKEN='supersecrettoken'

RUN pip install -U aiogram

COPY . .

ENTRYPOINT ["python", "main.py"]