FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["cd", "configs"]
CMD ["alembic", "upgrade", "head"]

CMD ["python", "main.py"]