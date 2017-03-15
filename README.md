# wefill

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
