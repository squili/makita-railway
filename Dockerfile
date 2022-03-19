FROM debian:latest

COPY . .

ENV HOST_ADDR=${HOST_ADDR}
ENV OWNER_ID=${OWNER_ID}
ENV TOKEN=${TOKEN}
ENV MANAGER_GUILD=${MANAGER_GUILD}
ENV GITHUB_WEBHOOK_SECRET=${GITHUB_WEBHOOK_SECRET}
ENV CLIENT_SECRET=${CLIENT_SECRET}
ENV CLIENT_ID=${CLIENT_ID}

RUN apt update && apt install -y python3 python3-pip && pip install -r requirements.txt && python3 main.py
