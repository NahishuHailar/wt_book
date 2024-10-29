up:
    docker-compose up -d

down:
    docker-compose down

build:
    docker-compose up --build -d

logs:
    docker-compose logs -f

migrate:
    docker-compose exec app alembic upgrade head

shell:
    docker-compose exec app bash
