FROM debian:latest

COPY . .

RUN apt update && apt install -y python3 python3-pip && pip install -r requirements.txt && python3 main.py
