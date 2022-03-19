FROM debian:latest

COPY . .

RUN apt update && apt install python3 && pip install -r requirements.txt && python3 main.py
