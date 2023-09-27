FROM python:latest
WORKDIR /root
COPY ./packages /root/packages
COPY ./.snowball.conf .
COPY ./main.py .
COPY ./Pipfile .
RUN pip install pipenv
RUN pipenv install
ENTRYPOINT [ "pipenv", "run", "./main.py"]