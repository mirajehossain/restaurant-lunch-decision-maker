# Lunch decision maker Service
To run the project set all the environment to a `.env` file. To run the project locally you need to setup `docker` and `docker-compose`.


## How to run the project
Simply do `docker-compose up --build --remove-orphans` to run the project. 


## Environments to run locally
```text=
DEBUG=True
SECRET_KEY=^fhr1j5jw6hp9y1^0v(%u69yhj!1cnl=xn4%3p4mciqzufxbg4

DB_NAME=lunch
DB_USER=lunch
DB_PASS=12345
DB_HOST=db
DB_PORT=5432

REQUEST_TIMEOUT=10
```


