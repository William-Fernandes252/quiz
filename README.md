# Quiz

A quiz application for the technical test for a developer position at Leantech.

![Question](./screenshots/main.png)
![Results](./screenshots/results.png)

## Run locally

-   install [Docker and Docker Compose](https://docs.docker.com/engine/install/) in your machine (I recommend installing Docker Desktop);
-   navigate to the project backend directory;
-   create a `.env` file with the content

        SECRET_KEY="django-insecure-wrmzj#y4o_-pn2!95wn+8(txrv5r9i$mho(%6*o)b4s4=_k31p"
        DEBUG=1
        ALLOWED_HOSTS=*

        POSTGRES_DB=quiz
        POSTGRES_USER=django
        POSTGRES_PASSWORD="EyQibMcmmZTkYk4thw6bJHuzYduwG6Sjzqiad9XNFQnP7knrFE5Q5JHftTqAPeiMrqLkAbebT49MwYRAa9DAe5RQNDNxoa5kTNwukYxE4kGpwC3fbYD7H4D7faAdsAAf"
        POSTGRES_HOST="127.0.0.1"

        DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}

-   run

        docker compose --file docker-compose.local.yml up -d

-   to run the project tests, run

        docker compose exec django pytest

