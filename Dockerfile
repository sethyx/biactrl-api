FROM --platform=linux/arm64 python:slim

RUN pip install flask

COPY . .

CMD python -u api.py