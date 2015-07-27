# Logpot
_(This is currently a very prototype version.)_

Logpot is a simple blog system build with flask.

## Getting Started
_It will need Python 3.x to get started._

Clone the repository
```
$ git clone https://github.com/mrjoes/flask-admin.git
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

initialize database
```
$ python manage.py initialize
```

run
```
$ honcho start
```
