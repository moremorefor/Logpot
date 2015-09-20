# Logpot
_(This is currently a very prototype version.)_

Logpot is a simple blog system build with flask.

## Getting Started
_It will need Python 3.x to get started._

Clone this repository
```
$ git clone git@github.com:moremorefor/Logpot.git
$ cd logpot
```

Create and activate a virtual environment
```
$ virtualenv env
$ source env/bin/activate
```

Setup
```
$ pip install -r ./requirements/dev.txt
$ bundle install --path vendor/bundle
$ npm install
$ bower install
$ gulp install
```

Edit database URI in config.py
```
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/logpot'
```

Initialize database
```
$ python manage.py initialize
```

run
```
$ honcho start
```
