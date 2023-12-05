# Summary

I'm glad to introduce to you brand-new (*propably not*) booking API.

In this project I've used `Django`, `drf`, `djoser` and `drf-spectacular`.\
Side technologies `Docker`, `docker-compose` and `PostgreSQL`.

This file will guide you through installation steps.

# Installation

### Setup virtual environment
```bash
$ python3 -m venv "dir/to/venv/"
```

### Clone

Simply clone repository to you directory on your drive by using following command:

```bash
$ git clone "https://github.com/simonari/bewise.ai-contest.git" "/dir/to/save"
```

### Configuring environment variables

Head down to `.env` file and configure field by your own.

`.env file`

```
DJANGO_SECRET_KEY=<YOUR SECRET>

DB_CONTAINER='booking_pg'
DB_VOLUME='.pgdb/'
DB_NAME='booking'
DB_USER=<YOUR USERNAME>
DB_PASSWORD=<YOUR PASSWORD>

DOCKER_NETWORK='booking'
```

### Compose database container

Head down to your directory and run this:

```bash
$ docker-compose up -d
```

### Install requirements 

```bash
$ pip install -r requirements.txt
```

### Add superuser

```bash
$ python manage.py createsuperuser 
```

### Now we should create tables

You've copied project's repository, so you don't have any tables yet!\
Run following commands to do that:

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

### That's time to start

```bash
$ python manage.py runserver
```

# Docs

Navigate to [127.0.0.1:8000/docs]() to check list of endpoints.\

There is a lot of [djoser](https://djoser.readthedocs.io/en/latest/index.html) endpoints that I haven't described but at
`Booking` section you can see 4 main endpoints.

# Auth

All of this stuff contained in [djoser](https://djoser.readthedocs.io/en/latest/index.html) docs.\
One thing, that I want to mention, is that this app uses `TokenAuthentication`.

# Contact

With any questions you can email me at [vsimonari@gmail.com]().