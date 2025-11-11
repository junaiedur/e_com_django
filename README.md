# E Commerce Project

### Setup E Commerce Project

- Create Virtual Environment:

```sh
python -m venv venv_ecom
```

- Activate Virtual Environment from commnad prompt:

```sh
venv_ecom\Scripts\activate
```

- Deactivate Virtual Environment from command prompt:

```sh
deactivate
```

You need to start virtual environment everytime before you run: `python manage.py runserver`
If you install any new packages before deactivating the virtual environment run: `pip freeze > requirements.txt`
For database setup, use `mysql`, then from cmd run:
```sh
python manage.py createsuperuser
python manage.py migrate
```
