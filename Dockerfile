FROM python:3.10-slim-buster

RUN apt update --no-install-recommends -y

RUN mkdir /src
COPY /src /src
COPY /src/main.py main.py
COPY /requirements.txt requirements.txt

RUN pip install -r /requirements.txt

CMD ["python3", "main.py"]
