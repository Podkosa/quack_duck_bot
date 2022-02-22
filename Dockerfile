FROM python:3.10

WORKDIR /duck_bot
ENV TGBOT_API_TOKEN='5190476214:AAFIaIb-8VyvXgGsatnndXRrap3evUGsOyI'

RUN pip install -U aiogram

COPY . .

ENTRYPOINT ["python", "main.py"]