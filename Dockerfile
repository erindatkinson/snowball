FROM python:latest
WORKDIR /root
COPY . .
RUN pip install pipenv
RUN pipenv install
ENTRYPOINT [ "pipenv", "run", "./main.py"]