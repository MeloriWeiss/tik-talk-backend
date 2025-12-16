# TikTalk

The backend application for a social network uses a microservice architecture and the RabbitMQ message broker to exchange data between services

## Development server

To launch the application, you need:

1) Run `docker-compose build` to build containers
2) Run `docker-compose up` to start containers

## Database preparation

Run the last `4` commands from the `Makefile's` from each microservice directory

## Using the app

1) Go to `http://localhost:15672/` to use RabbitMQ interface
2) Go to `http://localhost:8001/docs#/` to use `auth_service` Swagger docs
3) Go to `http://localhost:8002/docs#/` to use `main_service` Swagger docs
4) Go to `http://localhost:8003/docs#/` to use `chats_service` Swagger docs
5) Go to `http://localhost:5050` to use `pgAdmin`