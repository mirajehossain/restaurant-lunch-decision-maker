# Lunch decision maker Service
To run the project set all the environment to a `.env` file. To run the project locally you need to setup `docker` and `docker-compose`.


# How to run the project

## Environment variables
```text=
DEBUG=True
SECRET_KEY=^fhr1j5jw6hp9y1^0v(%u69yhj!1cnl=xn4%3p4mciqzufxbg4

DB_NAME=restaurant
DB_USER=restaurant
DB_PASS=12345
DB_HOST=db
DB_PORT=5432

REQUEST_TIMEOUT=10
```

## Run project 
```shell script
docker-compose up --build --remove-orphans // to run project in docker
docker-compose exec app bash //exec into docker image
cd src // change directory to src
./manage.py migrte // run apply migrations
```



# API documentation

HackMD: `https://hackmd.io/0QHAWxiHToStUTtVweBiQA?view`
