FROM python:3.11-rc-slim

RUN pip install poetry>=1.0.0
COPY app/ app/
RUN cd app && poetry install
WORKDIR app/
CMD ["poetry", "run", "gunicorn", "--bind=0.0.0.0:8080", "wsgi:app"]
