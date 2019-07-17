# Logpot

_(This is currently a very prototype version.)_

Logpot is a simple blog system build with flask.

## Getting Started

Clone this repository

```
$ git clone git@github.com:moremorefor/Logpot.git
$ cd logpot
```

Create and activate a virtual environment

```
$ python -m venv /path/to/new/virtual/env
$ source /path/to/new/virtual/env/bin/activate
```

Setup

```
$ pip install -r ./requirements/dev.txt
$ bundle install --path vendor/bundle
$ yarn
$ npx bower install
$ npx gulp install
```

Initialize database

```
$ python manage.py initialize
```

run

```
$ honcho start
```

### Set environment variables

If you want to change config, create `.env` file.

```
$ cat >.env <<EOF
LOGPOT_CONFIG=production
SECRET_KEY=hard to guess string
DATABASE_URI=postgresql://username:password@localhost/logpot
EOF
```
