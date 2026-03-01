FROM python:3.12.12-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app


COPY requirements.txt /app/


WORKDIR /var
RUN python -m venv venv/ --prompt openwheelalpha


WORKDIR /app


RUN pip install --upgrade 'pip<25.3' --no-cache-dir
RUN pip install -U setuptools psycopg2-binary --no-cache-dir
RUN pip install -r requirements.txt --no-cache-dir


COPY . .


EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

