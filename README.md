# Profiles REST API

### Creating Vagrant server

Run

```sh
vagrant init ubuntu/bionic64
```

Replace Vagrantfile code by the code of this [link](https://gist.github.com/LondonAppDev/199eef145a21587ea866b69d40d28682)

---

### Start Vagrant server

Run

```sh
vagrant up
```

---

### Connect Vagrant server

Run

```sh
vagrant ssh
```

---

### How to disconnect Vagrant server

Run

```sh
exit
```

---

### To connect Vagrant server after restarting machine

Run

```sh
vagrant reload
vagrant ssh
```

---

### Create Python Virtual Enviroment

Run

```sh
vagrant@ubuntu-bionic:$ cd /vagrant
vagrant@ubuntu-bionic:/vagrant$ python -m venv ~/venv
```

The reason we are using ~ because we want our virtual environment only in the server, not in our local machine.

---

### Activate Virtual Enviroment

Run

```sh
vagrant@ubuntu-bionic:/vagrant$ source ~/venv/bin/activate
```

---

### Install required Python packages

Run

```sh
(venv) vagrant@ubuntu-bionic:/vagrant$ touch requirements.txt

```

Write in requirements.txt

```sh
django==3.0.7
djangorestframework==3.11.0

```

Install requirements.txt

```sh
(venv) vagrant@ubuntu-bionic:/vagrant$ pip install -r requirements.txt
```

---

### Create Django project

Run

```sh
(venv) vagrant@ubuntu-bionic:/vagrant$ django-admin.py startproject profiles_project .

```

The reason we want to put dot, because we want to create project in Root folder.

---

### Create an app

Run

```sh
(venv) vagrant@ubuntu-bionic:/vagrant/profiles_project$ python manage.py startapp profiles_api

```

---

### Enable our app

Goto profiles_project > profiles_api > profiles_project > settings.py
append rest_framework and rest_framework.authtoken in INSTALLED_APPS list.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
]
```

Now we will our app name in INSTALLED_APPS list.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'profiles_api',
]
```

---

### Start Django development web server

Run

```sh
(venv) vagrant@ubuntu-bionic:/vagrant$ python manage.py runserver 0.0.0.0:8000

```

0.0.0.0 is making available on all network adapters and :8000 is for starting in Port 8000. In our Vagrant file, we mapped 8000 on our host machine, that's why we specify Port 8000 when we start the server.

Start browser and goto [127.0.0.1:8000](http://127.0.0.1:8000/)

---
