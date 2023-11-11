FROM --platform=linux/arm64 python:3.11-slim-bookworm

RUN pip install flask

COPY . .

CMD python -u api.py