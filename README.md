# Bibliotek_System
Oppgave rundt bruk av databaser i python med bruk av django. Hensikt å kunne lage en database med fokus på CRUD operasjoner.

Oppgave rundt bruk av databaser i python med bruk av django. Hensikt\
å kunne hente ut informasjon fra ulike tabeller og analysere innholdet.\
Deretter formatere det og lagre det som sql filer. 

**Libraries som må lastes ned i forkant eller underveis:**
- python 3.12.7 eller 3.13.2
- django 5.1.6
- matplotlib
- psycopg2
- tabulate
- numpy

Docker desktop eller tilsvarende vil også være nødvendig.

**Forberedelser:**\
Åpne en cmd vindu og sett opp virtual environmnet på ønsket plassering med: \
``py -m venv [virtual_environment_navn]``\
og aktiver med:\
``Srcipt\activate.bat``

Installer de ulike libraries med:\
``pip install django==5.1.6``\
``pip install psycopg2 matplotlib tabulate numpy``

start nytt django prosjekt med:\
``django-admin startproject [prosjekt_navn]`` 

i prosjekt mappen skal man se følgende:
```
[prosjekt_navn] <- mappe
manage.py
```

Lag en django-app med:\
``py manage.py [app_navn]``

Legg til følgende filer, ``models.py`` og ``admin.py`` fra mappen ``bibliotek`` i din\ 
egen app mappen ``[app_navn]`` som ble laget i steget ovenfor. Det er også mulig å\
kopiere over innholdet til filene med samme navn.

Deretter gå til ``[prosjekt_navn]/settings.py`` og endre følgende
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
til 
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_navn'
]
```

Gå tilbake til ``[prosjekt_navn]`` mappen og bruk:\
``py manage.py makemigrations [app_navn]``\
``py manage.py migrate``

### Valgfritt
Bruk\
``py manage.py createsuperuser``\
og legg til brukernavn, email og passord for å lage admin bruker. Bruk:\
``py manage.py runserver``\
og skriv inn:\
``127.0.0.1:8000/admin/``\
i en nettleser. Man kan gå inn for å se at alt er som det skal, men er ikke nødvendig.\
For å stoppe/lukke serveren bruk:\
``ctrl + c``

På dette stadiet er oppsettet med Django ferdig. legg til mappen ``support text``,\
og filen ``help.json``, ``edit_menu.json`` i mappen. I ``[prosjekt_navn]`` legg til\
``main.py``, og mappen ``classes``, inkludert alt innholdet som kan bli funnet fra\ 
denne github siden.\
Filene i mappen ``[prosjekt_navn]`` skal være tilsvarende som:
```
- prosjekt_navn:
    - app_navn:
        - migrations:
            - __init__.py
            - 0001_initial.py
        - __init__.py
        - admin.py
        - apps.py
        - models.py
        - tests.py
        - views.py
    - classes:
        - analytic.py
        - author_query.py
        - base.py
        - book_query.py
        - borrowing_query.py
        - category_query.py
        - customer_query.py
        - interface.py
        - library_query.py
    - prosjekt_navn:
        - __init__.py
        - asgi.py
        - settings.py
        - urls.py
        - wsgi.py
    - support text:
