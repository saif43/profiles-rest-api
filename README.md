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

### When to use API View

- **Need full control over the logic**. Such as when wr are running a very complicated algorithm or updating multiple data sources in one API call.
- **Processing files and rendering a synchronous response.** Such as validating a file and returning the result in a same call.
- **Calling other APIs/services.** Another time when we can use it, when we are calling other external APIs or services in the same request.
- **Accessing local files or data**

---

### Create first API View

Goto views.py and erase everything. Then write

```python
from rest_framework.views import APIView
from rest_framework.response import Response


class HelloApiView(APIView):
    """Test API View"""

    def get(self, request, format=None):
        result = [1, 2, 3, 4, 5]

        return Response({"message": "Hello", "result": result})

```

---

### Configure view URL

In profiles_api create urls.py

```python
from django.urls import path
from profiles_api import views

urlpatterns = [
    path("hello-view/", views.HelloApiView.as_view()),
]
```

then goto profiles_projects > urls.py and write

```python
from django.urls import include, path

```

Include is a function that we can use to include urls from other apps in the root projects.

In urlpatterns list, append this code

```python
path("api/", include("profiles_api.urls")),
```

---

### Create a Serializer

If we are going to add POST or UPDATE functionality to our Hello API View, then we need to create a serializer to receive the content we post to the API.
Let's create "serializers.py" file in our profiles_api app.

What we're gonna do is we're gonna create a simple serialize that accepts a name input and then we're going to add this to our API view and we're gonna use it to test the post functionality of our API view.

```python
from rest_framework import serializers


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""

    name = serializers.CharField(max_length=10)

```

---

### Add POST method to APIView

Let's go to our "views.py" and import status from rest_framework and our serializer module from "serializers.py".

The status object from rest_framework is the list of HTTP status codes that we can use when returning responses from our API.

We are going to use the serializer module to tell our API view what data to expect when making post, put and patch requests.

Now we'll write our post method

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from profiles_api import serializers


class HelloApiView(APIView):
    """Test API View"""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        result = [1, 2, 3, 4, 5]

        return Response({"message": "Hello", "result": result})

    def post(self, request):
        """Create a post request with our name"""

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            msg = f"Hello {name}"
            return Response({"message": msg})
        else:
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


```

The self.serializer_class function is a function that comes with the API view that retrieves the configured serializer class for our view. So it's the standard way we should retrive the serializer class when working with serialzer in a view.

Next we go ahead and validate our serializer. It means, we are going to ensure that the input is valid as per as the specification of our serializer fields.

In our case we are validating that our name is no longer then 10 characters.

---

### Add PUT, PATCH and DELETE methods

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from profiles_api import serializers


class HelloApiView(APIView):
    """Test API View"""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        result = [1, 2, 3, 4, 5]

        return Response({"message": "Hello", "result": result})

    def post(self, request):
        """Create a post request with our name"""

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            msg = f"Hello {name}"
            return Response({"message": msg})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({"method": "PUT"})

    def patch(self, request, pk=None):
        """Handle partial update of an object"""
        return Response({"method": "PATCH"})

    def delete(self, request, pk=None):
        """Handle updating an object"""
        return Response({"method": "DELETE"})

```

---

## ViewSets

Gives us control over:

- Takes care of a lot of common logic
- Perfect for standard database operations
- Fastest way to make an API which interfaces with a database backend

### When to use API View

- **CRUD**. If we need to write an API that performs a simple CREATE, READ, UPDATE and DELETE operation on an existing database model.
- **A quick and simple API** Quick and simple API to manage a predefiend objects.
- **No customization on the logic** Very basic custom logic additional to the view set featrues already provided by Django REST Framework.
- **Working with simple database structure**

---

### Create a simple Viewset

In views.py, import viewsets from rest_framework then, write

```python
class HelloViewSet(viewsets.ViewSet):
    """Test API viewset"""

    def list(self, request):
        """return a Hello msg"""
        result = [1, 2, 3, 4, 5]
        result.append("View set")

        return Response({"message": "Hello", "result": result})
```

---

### Add URL router

Registering Viewset in URL is slightly differnt from APIView.

So with Viewset we may be accessing the list request, which is just the route of our API. And in this case we would use a differnt URL than if we are accessing the specific object to do an UPDATE, a DELETE or a GET.

Import include django.urls, include used for including list of URLs in the URL pattern and assigning the lists to a specific URL.

Next import DefaultRouter from rest_framework.routers, it's used to register URL.

```python
from django.urls import path, include
from profiles_api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("hello-viewset", views.HelloViewSet,basename="hello-viewset")

urlpatterns = [
    path("hello-view/", views.HelloApiView.as_view()),
    path('', include(router.urls))
]

```

In router.register function,

1st argument is the name of the URL we wish to create. We have given "hello-viewset", we are going to access our API using "hello-viewset". Router will create all of the 4 URLs for us. So we don't need to use any '/' forward slash here.

2nd argument is the viewset, we wish to register in this URL.

3rd argument is the basename, this is going to be used for retriving the URL in our router.

In urlpatterns add `path('', include(router.urls)`

As we registered new route with router, it generates a list of URLs that are associated for our view set. It figures out the URLs that are REQUIRED for all of the functions that we add to our VIEWSET, then it generates the URL list which we can pass in using PATH and INCLUDE function.

We have put empty string, because we don't want to put any prefix to this URL.

---

### Add create, retrieve, update, partial_update and destroy functions

Open view.py and in HelloViewSet class..

```python
class HelloViewSet(viewsets.ViewSet):
    """Test API viewset"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """return a Hello msg"""
        result = [1, 2, 3, 4, 5]
        result.append("View set")

        return Response({"message": "Hello", "result": result})

    def create(self, request):
        """Create a Hello msg"""

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f"Hello {name}"

            return Response({"message": message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle getting an object by ID"""

        return Response({"HTTP method": "GET"})

    def update(self, request, pk=None):
        """Update an object by ID"""

        return Response({"HTTP method": "PUT"})

    def partial_update(self, request, pk=None):
        """Update an object by ID"""

        return Response({"HTTP method": "PATCH"})

    def destroy(self, request, pk=None):
        """delete an object by ID"""

        return Response({"HTTP method": "DELETE"})

```

To see the list of object, hit `http://127.0.0.1:8000/api/hello-viewset/` with get method.

We can also create an object from here. But Unlike the API view we don't actually see the PUT, PATCH and DELETE methods here on the Hello-ViewSet API.

Viewset expect that we use `http://127.0.0.1:8000/api/hello-viewset/` endpoint to retrive a list of objects in the database, and we will specify a Primary Key ID in the URL when making the changes to a specific object.

So according to use the RETRIEVE, UPDATE, PARTIAL_UPDATE, DESTROY methods, we need to specify a primary key at the end of the URL.

Example: `http://127.0.0.1:8000/api/hello-viewset/1/`

---

## Creating Profile API

### Purpose

1. Create a new Profile

   - Handle registration of new users
   - Validate profile data

2. Listing existing profiles

   - Search for profiles
   - Email and name

3. View specific profiles

   - Using profile ID

4. Update profile of logged in user
   - Change name, email and password
   - Delete own profile

| API URLs                   | Purpose                                                                                                                                                              |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `api/profile`              | <ul><li>list all profiles when HTTP GET method is called</li><li>create new profile when HTTP POST method is called</li></ul>                                        |
| `api/profile/<profile_id>` | <ul><li> View specific profile details by using HTTP GET </li> <li> update object using HTTP PUT / PATCH </li> <li> remove it completely using HTTP DELETE </li><ul> |

---

### Create user profile serializer

Let's create UserProfileSerializer in `serializer.py`. We are going to use **ModelSerializer** as a base class and we'll get them connected up to our UserProfile model. But why **ModelSerializer** ???

**ModelSerializer** is very similer to a regular serializer except it has a bunch of extra functionality which makes it really wasy to work with Django Database Model.

```python
from rest_framework import serializers
from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""

    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serialize a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ("id", "email", "name", "password")
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

    def create(self, validated_data):
        """Create and return a new user"""

        user = models.UserProfile.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            password=validated_data["password"],
        )

        return user
```

The way that we work with **ModelSerializer** is, we use a **meta** class to configure the serilizer to point a specific model in our project.

`model = models.UserProfile` sets our serilizer up to point our UserProfile model.

`fields = ("id", "email", "name", "password")`, So this is a list of all the field that we want to make accessible in our API.

`extra_kwargs` is for custom configuration.

ModelSerializer provides default **Create** function. But we want to override this Create function and use our user create_user function. Because we want our Password to be hashed.

---

### Create profile ViewSet

Let's create a viewset to access the serilizer. Go to `views.py` and import models.

We are going to use ModelViewSet as base class, which is specifically designed for managing models through API.

```python
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
```

The way we work with the ModelViewSet is that, we connect a serializer class and provide a **queryset** so that it knows which objects in the database are gonna be managed through this viewset.

The Django REST Framework knows the standard function that we want to perform on a model view set, and that is the CREATE, LIST, UPDATE, PARTIAL_UPDATE and DESTROY. Django REST Framework takes care of all of this for us just by assigning these Serializer class to model serializer and the queryset.

---

### Register profile Viewset with the URL

```python
from django.urls import path, include
from profiles_api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("hello-viewset", views.HelloViewSet, basename="hello-viewset")
router.register("profile", views.UserProfileViewSet)

urlpatterns = [
    path("hello-view/", views.HelloApiView.as_view()),
    path("", include(router.urls)),
]

```

Unlike the HelloViewSet, we don't need to specify basename for our Profile viewset. Because in `UserProfileViewSet` we have provided queryset. If we provide queryset, then Django rest framework can figure out the name from the model that's assigned to it.

---

### Create Permission Class

We don't want any user to modify another user's data. That's why we are creating permission class. Create `permissions.py` under profiles_api.

```python
from rest_framework import permissions


class UserOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profiles"""

    def has_object_permission(self, request, view, obj):
        """check if user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.id == obj.id

```

---

### Add authentication and permission in view.py

In `views.py` import TokenAuthentication from rest_framework.authentication and permission.py. Then make some changes into `UserProfileViewSet`

```python
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UserOwnProfile,)


```

---

### Add Search profiles features

| API URLs                    | Purpose             |
| --------------------------- | ------------------- |
| `api/profile/?search=query` | Search User profile |

In `views.py` import filters from rest_framework. Then make some changes into `UserProfileViewSet`

```python
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UserOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        "name",
        "email",
    )

```

So in the browser we'll be able to see a Filter button. But as a API, we need to goto `http://127.0.0.1:8000/api/profile/?search=query` for search any particular user.

---

### Create login API viewset

| API URLs            | Purpose     |
| ------------------- | ----------- |
| `api/profile/login` | User log in |

In `views.py`

```python
# add imports
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication token"""

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


```

ObtainAuthToken is view which comes with Django framework, that we can use to generate authtoken.

ObtainAuthToken can be added in URLs. However it doesn't BY DEFAULT enable itself in browsable Django admin site.

So we need to customize it to browsable API, so that we can test this.

`renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES` what it does is, it addes renderer class in ObtainAuthToken. ObtainAuthToken does't come with renderer class by default. That's why we had to add to manually.

Now goto `urls.py`

Add `path("login/", views.UserLoginApiView.as_view()),` in urlpatterns.

---

## Creating Profile Feed API

### Purpose

1. Create new feed items for authenticated users

2. Updating feed items for authenticated users

3. Deleting feed items for authenticated users

4. Viewing other users feed

| API URLs                  | Purpose                                                                                                                                      |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `api/feed`                | <ul><li>GET (List of feed items) </li><li>POST (create feed items for authenticated users) </li></ul>                                        |
| `api/feed/<feed_item_id>` | <ul><li> GET (getting specific feed item) </li> <li> PUT / PATCH (for updaing a feed item)</li> <li> DELETE (deleting a feed item) </li><ul> |

---

### Add Profile feed item Model

Goto `models.py` and add

```python
from django.conf import settings

class ProfileFeedItem(models.Model):
    """Profile status update"""

    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """return model as a String"""
        return self.status_text

```

We could have write `"UserProfile"` instead of `settings.AUTH_USER_MODEL`. While we are using Auth user model, it's **Best Practice** to use `settings.AUTH_USER_MODEL`. Because if we decide to swap different model then the relationships would automatically be updated without us having to go through and manually change it everywhere that we referenced in our `models.py` file.

---

### Model migration

Since we did make some changes in `models.py`, we need to run migrations.

```
(venv) vagrant@ubuntu-bionic:/vagrant/profiles_project$ python manage.py makemigrations
(venv) vagrant@ubuntu-bionic:/vagrant/profiles_project$ python manage.py migrate
```

---

### Register the model

Goto `admin.py` and add,

```python
admin.site.register(models.ProfileFeedItem)
```

---

### Create Profile Feed Item Serializer

Goto `serializer.py` and add,

```python
class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serialize a profile feed item object"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ("id", "user_profile", "status_text", "created_on")
        extra_kwargs = {"user_profile": {"read_only": True}}
```

---

### Create viewset of Profile Feed Item

Goto `views.py` and add

```python
class ProfileFeedItemView(viewsets.ModelViewSet):
    """Handling creating, reading, updating profile feed item"""

    serializer_class = serializers.ProfileFeedItemSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = models.ProfileFeedItem.objects.all()

    def perform_create(self, serializer):
        """Sets the user as Logged in user"""
        serializer.save(user_profile=self.request.user)
```

The `perform_create` is a handy function which comes with Django Rest Framework, that allows you to override the behavior or customize the behavior for creating objects through a model viewset.

So when a request gets made to our viewset, it gets passed into our serialied class and validated and then serializer.save() is called by default.

If we need to customize the logic for creating an object then we can perform this `perform_create` function.

Here we want to put the id of authenticated user, that's why we are passing `user_profile=self.request.user`.

The request object is an object that gets passed into all view sets every time a request is made and as the name suggests it contains all of the details about the request being made to the view set because we've added the token authentication to our view set if the user has authenticated then the request will have a user associated to the authenticated user.
So this user this user field gets added whenever the user is authenticated.

Now lets's link up our viewset in to `urls.py`. Goto `urls.py` and add,

```python
router.register("feed", views.ProfileFeedItemView)
```

---

### Add permission for Feed API

We want two kind of permissions.

1. User will be able to update their own feed.

2. If the user is not authenticated then feeds will be in read only mood.

goto `permissions.py` and add,

```python
class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to add their own status"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id
```

Goto `views.py` and merge this permission in `ProfileFeedItemView` class.

```python
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ProfileFeedItemView(viewsets.ModelViewSet):
    """Handling creating, reading, updating profile feed item"""

    serializer_class = serializers.ProfileFeedItemSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        permissions.UpdateOwnStatus
    )

    def perform_create(self, serializer):
        """Sets the user as Logged in user"""
        serializer.save(user_profile=self.request.user)
```

`IsAuthenticatedOrReadOnly` makes sure, if there is no authenticated users, then feeds will be in show only mode.

And `UpdateOwnStatus` will make sure that a user can't update another user's feed.

If we want to show our feeds to our authenticated users only, then we will use `IsAuthenticated` instead of `IsAuthenticatedOrReadOnly`.

---
