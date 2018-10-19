# wefill

[![GuardRails badge](https://badges.production.guardrails.io/gitsignore/wefill.svg)](https://www.guardrails.io)

Wefill is an educational project to order fuel online.

Require wefill-api : <https://github.com/TataneInYourFace/wefill-api>

## Requirements

- Python
- pip install Django
- pip install requests
- pip install django-widget-tweaks
- pip install django-paypal
- [wefill-api](https://github.com/TataneInYourFace/wefill-api)

## Installation

First, you need to clone this repository:
```bash
$ git clone https://github.com/TataneInYourFace/wefill.git
```

Go in the application folder:
```bash
$ cd wefill
```

Copy settings file and edit it with your options like `SECRET_KEY`:
```bash
$ cp wefill/settings.py.dist wefill/settings.py
```

Execute the server:
```bash
$ python manage.py runserver
```

In your browser go to : http://127.0.0.1:8000

## Screenshot
Home page:

![](https://github.com/TataneInYourFace/wefill/blob/master/readme-sources/home.gif?raw=true)

Error 404:

![](https://github.com/TataneInYourFace/wefill/blob/master/readme-sources/err404.gif?raw=true)

Booking:

![](https://github.com/TataneInYourFace/wefill/blob/master/readme-sources/book.gif?raw=true)

Profile:

![](https://github.com/TataneInYourFace/wefill/blob/master/readme-sources/account.gif?raw=true)
