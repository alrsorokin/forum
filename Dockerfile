FROM python:3.6-slim AS backend

ENV TZ Europe/Moscow
ENV PYTHONDONTWRITEBYTECODE yes

RUN mkdir /app
ENV HOME=/app
ENV PYTHONPATH=$HOME
WORKDIR $HOME

COPY configurations/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

COPY configurations/config.py .
COPY forum $HOME/forum
