FROM ubuntu:18.04
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip libpq-dev netcat-openbsd
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN chmod +x ./entrypoint.sh
CMD ["./entrypoint.sh"]
