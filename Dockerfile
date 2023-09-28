FROM python:latest
RUN apt update && apt upgrade
RUN apt install -y dc
WORKDIR /root
COPY ./packages /root/packages
COPY ./.snowball.conf .
COPY ./main.py .
COPY ./Pipfile .
RUN pip install pipenv
RUN pipenv install
ENTRYPOINT [ "pipenv", "run", "./main.py"]