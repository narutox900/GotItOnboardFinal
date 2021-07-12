# GotItOnboardFinal

## Installation

1. Initialize and activate a virtual environment

```
$ python3 -m venv env
$ source env/bin/activate
```

2. Install dependencies

```
$ pip install -r requirements.txt
```

## Usage

1. Start the database

```
$ docker-compose up
```

2. Set environment variable

```
$ export FLASK_ENV=development # development, production
```

3. Initialize database

```
$ flask init-db
```

4. Run the server

```
$ flask run
```

## Shut down the database

```
$ docker-compose down
```

## Run tests

```
$ bash test.sh
```

## Clear database

```
$ flask clear-db
```

## Hard reset database

```
$ docker-compose down -v
$ docker-compose build
$ docker-compose up
```