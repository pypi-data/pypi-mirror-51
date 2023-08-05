djangorestframework_emailuser
=============================

.. image:: https://travis-ci.org/simlist/django-rest-framework-emailuser.svg?branch=master
    :target: https://travis-ci.org/simlist/django-rest-framework-emailuser

.. image:: https://coveralls.io/repos/github/simlist/django-rest-framework-emailuser/badge.svg?branch=master
    :target: https://coveralls.io/github/simlist/django-rest-framework-emailuser?branch=master

Overview
--------

A user for djangorestframework that uses an email as the username.

Features
--------

* Use email as username for loging in
* One name field instead of first name and last name
* Endpoints for creating an account, viewing, and updating accounts
* Django admin to work with EmailUser model.

Requirements
------------

- Python 3.5+
- Django 2.2+
- Djangorestframework 3.10+

Installation and Configuration
------------------------------

Install using ``pip``:

.. code-block:: sh

  $ pip install djangorestframework_emailuser

Add ``'emailuser'`` to ``INSTALLED_APPS``:

.. code-block:: Python

  # mysite/settings.py
  INSTALLED_APPS = [
      ...
      'emailuser',
  ]

Add the following line to ``settings.py`` to override django's default User
model with the 'EmailUser' model:

.. code-block:: Python

  # mysite/settings.py
  AUTH_USER_MODEL = 'emailuser.EmailUser'

Add urls to url conf:

.. code-block:: Python

  # mysite/urls.py
  from django.urls import path, include
  urlpatterns = [
    ...
    path('accounts/', include('emailuser.urls')),
  ]

Using
-----
To create a user programatically:

.. code-block:: Python

  from django.contrib.auth import get_user_model

  normal_user = get_user_model().objects.create_user(
      email='me@example.com',
      name='My Name',
      password='MyPassword'
  )

  superuser = get_user_model().objects.create_superuser(
      email='admin@example.com',
      name='Super Name',
      password='MySuperPassword'
  )

Using Endpoints:
~~~~~~~~~~~~~~~~
Assuming emailuser urls were set to ``/accounts/``:

Creating user
?????????????
``POST`` ``{"email": email, "name": name, "password": password}``
to ``/accounts/users/register``

Updating User
?????????????
``PUT`` ``{"email": email, "name": name, "password": password}``
to ``/accounts/users/<int:pk>/``
or
``PATCH`` the attribute you want to change
to ``/accounts/users/<int:pk>/``

Referencing User
????????????????
To reference user object in your code as a string (As for foreign keys):

.. code-block:: Python

  from django.conf import settings

  user_model = settings.AUTH_USER_MODEL

To reference the user class directly:

.. code-block:: Python

  from django.contrib.auth import get_user_model

  user_model = get_user_model()

See `Django docs <https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#referencing-the-user-model>`_  for more details.

Attributes
~~~~~~~~~~
The EmailUser model has the following attributes:

email
  The email address used as the login username.

name
    A single field for the name of the user.
password
  The password is hashed as set by the django settings.

is_superuser
  A boolean attribute that can only be set programatically.

is_staff
  A boolean attribute that can be set by the admin site or
  programatically.

EmailUser also subclasses ``django.contrib.auth.models.PermissionsMixin``.
