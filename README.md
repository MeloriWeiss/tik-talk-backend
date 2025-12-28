# TikTalk

The backend application for a social network uses a microservice architecture and the RabbitMQ message broker to exchange data between services

## Development server

To launch the application, you need:

1) Run `docker-compose build` to build containers
2) Run `docker-compose up` to start containers

## Databases preparation

Services, database connections, migrations creation and application, and seeding will be performed `automatically`

## Application management

The main commands for managing microservices are listed in the `Makefile` located in each service's directory

You can execute these commands from `any` directory since the operations are performed within `Docker` containers

## Using the app

1) Go to `http://localhost:15672/` to use RabbitMQ interface
2) Go to `http://localhost:8002/docs#/` to use `main_service` Swagger docs
3) Go to `http://localhost:8002/docs#/` to use `logging_service` Swagger docs
4) Go to `http://localhost:5050` to use `pgAdmin`