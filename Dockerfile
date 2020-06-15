FROM python:3.7.1

LABEL Author="Harriet Peel"
LABEL version="0.0.1"

ENV FLASK_APP="app.py"
ENV FLASK_ENV="development"
ENV FLASK_DEBUG True

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

ADD . /app

EXPOSE 5000

CMD flask run --host=0.0.0.0