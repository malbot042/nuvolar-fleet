FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /nuvolar-fleet-app
COPY requirements.txt /nuvolar-fleet-app/
RUN pip install -r requirements.txt
ADD . /nuvolar-fleet-app
