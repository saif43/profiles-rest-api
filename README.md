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

Now we will append our app name in INSTALLED_APPS list.

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

Start browser and goto 127.0.0.1:8000

---

### Creating database model

In models.py we are going to import AbstractBaseUser and PermissionsMixin from django.contrib.auth.models.

These are the standard base classes that you need to use when overwriting or customizing the default
Django user model.

```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for user"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrive full name for user"""
        return name

    def __str__(self):
        return email
```

---

### Adding user model manager

Now because we've customized I'll use a model we need to tell Django how to interact with this user model in order to create users because by default when it creates a user it expects a user name field and a password filled.
But we replace the user name field with an email field.
So we just need to create a custom manager that can handle creating users with an email field instead
of a user name field.

```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profile"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have an email")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser"""

        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for user"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrive full name for users in the system"""
        return name

    def __str__(self):
        return email

```

---

### Set our custom user model

Now that we've created our custom user model and our custom user model manager we can configure Django
project to use this as the default user model instead of the one that's provided by Django.

Goto profiles_project/settings.py and add

```python
AUTH_USER_MODEL = 'profiles_api.UserProfile'
```

at the bottom of the file.

---

### Create migrations and sync DB

Next we're going to create a Django migration file for our models that we've added to the project. So every time we change a model or add additional models to our projects we need to create a new migration file the migration file will contain the steps required to modify the database to match our updated models.

```python
(venv) vagrant@ubuntu-bionic:/vagrant/profiles_project$ python manage.py makemigrations profiles_api
(venv) vagrant@ubuntu-bionic:/vagrant/profiles_project$ python manage.py migrate
```

---

### Creating a Superuser

```python
(venv) vagrant@ubuntu-bionic:/vagrant/profiles_project$ python manage.py createsuperuser
```

Then enter email, name and password

---

### Enable Django Admin

Goto admin.py and import models of profiles api, and then register the model.

```python
from profile_api import models

admin.site.register(models.UserProfile)
```

Then enter email, name and password

---

## API View

Gives us control over:

- Perfect for implementing complex logic
- Calling other APIs
- Working with local files

### Enable Django Admin

- **Need full control over the logic**. Such as when wr are running a very complicated algorithm or updating multiple data sources in one API call.
- **Processing files and rendering a synchronous response.** Such as validating a file and returning the result in a same call.
- **Calling other APIs/services.** Another time when we can use it, when we are calling other external APIs or services in the same request. -**Accessing local files or data**
