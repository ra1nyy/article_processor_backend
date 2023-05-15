FROM python:3.11-slim

WORKDIR /backend
COPY . /backend

RUN chmod +x /backend/entrypoint.sh

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --deploy --system

CMD ["sh", "entrypoint.sh", "backend"]
