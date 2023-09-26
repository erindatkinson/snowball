FROM python:latest
COPY . .
RUN pip install pipenv
RUN pipenv install
ENTRYPOINT [ "pipenv", "run", "./main.py"]