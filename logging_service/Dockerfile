FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN echo "deb http://deb.debian.org/debian bullseye main" > /etc/apt/sources.list
RUN apt-get update && apt-get install -y netcat

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY start.sh /start.sh
RUN chmod +x /start.sh

COPY . .

ENTRYPOINT ["/start.sh"]

CMD ["/entrypoint.sh", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]