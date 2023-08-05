=============================
Django Elastic App Search
=============================

.. image:: https://badge.fury.io/py/django-elastic-appsearch.svg
    :target: https://badge.fury.io/py/django-elastic-appsearch

.. image:: https://travis-ci.org/CorrosiveKid/django_elastic_appsearch.svg?branch=master
    :target: https://travis-ci.org/CorrosiveKid/django_elastic_appsearch

.. image:: https://codecov.io/gh/CorrosiveKid/django_elastic_appsearch/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/CorrosiveKid/django_elastic_appsearch

.. image:: https://readthedocs.org/projects/django-elastic-appsearch/badge/?version=latest
    :target: https://django-elastic-appsearch.readthedocs.io/en/latest/?badge=latest

.. image:: https://badgen.net/dependabot/CorrosiveKid/django_elastic_appsearch?icon=dependabot
    :target: https://dependabot.com/

Integrate your Django Project with Elastic App Search with ease.

Documentation
-------------

The full documentation is at https://django_elastic_appsearch.readthedocs.io. Read our step-by-step guide on integrating App Search with your existing Django project over at Medium_.

.. _Medium: https://medium.com/@rasika.am/integrating-a-django-project-with-elastic-app-search-fb9f16726b5c

Dependencies
------------

* `elastic-app-search <https://pypi.org/project/elastic-app-search/>`_
* `serpy <https://pypi.org/project/serpy/>`_

Usage
-----
Installing
==========

Install Django Elastic App Search::

    pip install django_elastic_appsearch

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_elastic_appsearch',
        ...
    )

Add the Elastic App Search URL and Key to your settings module:

.. code-block:: python

    APPSEARCH_URL = 'https://appsearch.base.url'
    APPSEARCH_API_KEY = 'some_appsearch_api_token'

Configuring app search indexable models
=======================================

Configure the Django models you want to index to Elastic App Search. You can do this by inheriting from the ``AppSearchModel``, and then setting some meta options.

``AppsearchMeta.appsearch_engine_name`` - Defines which engine in your app search instance your model will be indexed to.

``AppsearchMeta.appsearch_serialiser_class`` - Defines how your model object will be serialised when sent to your elastic app search instance. The serialiser and fields used here derives from `Serpy <https://serpy.readthedocs.io/>`__, and you can use any of the serpy features like method fields.

Example:

.. code-block:: python

    from django_elastic_appsearch.orm import AppSearchModel
    from django_elastic_appsearch import serialisers

    class CarSerialiser(serialisers.AppSearchSerialiser):
        full_name = serialisers.MethodField()
        make = serialisers.StrField()
        model = serialisers.StrField()
        manufactured_year = serialisers.Field()

        def get_full_name(self, instance):
            return '{} {}'.format(make, model)


    class Car(AppSearchModel):

        class AppsearchMeta:
            appsearch_engine_name = 'cars'
            appsearch_serialiser_class = CarSerialiser

        make = models.CharField(max_length=100)
        model = models.CharField(max_length=100)
        manufactured_year = models.CharField(max_length=4)

Using model and queryset methods to index and delete documents
==============================================================

Then you can call ``index_to_appsearch`` and ``delete_from_appsearch`` from your model objects.

Send the car with id 25 to app search.

.. code-block:: python

    from mymodels import Car

    car = Car.objects.get(id=25)
    car.index_to_appsearch()

Delete the car with id 21 from app search.

.. code-block:: python

    from mymodels import Car

    car = Car.objects.get(id=21)
    car.delete_from_appsearch()

You can also call ``index_to_appsearch`` and ``delete_from_appsearch`` on QuerySets of ``AppSearchModel``

Send all cars where the make is 'Toyota' to app search.

.. code-block:: python

    cars = Car.objects.filter(make='Toyota')
    cars.index_to_appsearch()

Delete all cars where the make is 'Saab' from app search

.. code-block:: python

    cars = Car.objects.filter(make='Saab')
    cars.delete_from_appsearch()

Use with your own custom queryset managers
==========================================

If you want to specify custom managers which also has this functionality, you can inherit from ``django_elastic_appsearch.orm.AppSearchQuerySet``

.. code-block:: python

    from django_elastic_appsearch.orm import AppSearchModel, AppSearchQuerySet

    class MyCustomQuerySetManager(AppSearchQuerySet):
        def my_custom_queryset_feature(self):
            # Do Something cool
            pass

    class MyCustomModel(AppSearchModel):
        field_1 = models.CharField(max_length=100)

        # Set the custom manager
        objects = MyCustomQuerySetManager.as_manager()

Writing Tests
=============

This package provides a test case mixin called ``MockedAppSearchTestCase`` which makes it easier for you to write test cases against ``AppSearchModel``'s without actually having to run an Elastic App Search instance during tests.

All you have to do is inherite the mixin, and all the calls to Elastic App Search will be mocked. Example below.

.. code-block:: python

    from django.test import TestCase
    from django_elastic_appsearch.test import MockedAppSearchTestCase
    from myapp.test.factories import CarFactory

    class BookTestCase(MockedAppSearchTestCase, TestCase):
        def test_indexing_book(self):
            car = CarFactory()
            car.save()
            car.index_to_appsearch()

            self.assertAppSearchModelIndexCallCount(1)

You will have access to the following methods to check call counts to different mocked app search methods.

``self.assertAppSearchQuerySetIndexCallCount`` — Check the number of times index_to_appsearch was called on a appsearch model querysets.

``self.assertAppSearchQuerySetDeleteCallCount`` — Check the number of times delete_from_appsearch was called on an appsearch model querysets.

``self.assertAppSearchModelIndexCallCount`` — Check the number of times index_to_appsearch was called on an appsearch model objects.

``self.assertAppSearchModelDeleteCallCount`` — Check the number of times delete_from_appsearch was called on an appsearch model objects.

Using the elastic app search python client
==========================================

We use the official `elastic app search python client <https://github.com/elastic/app-search-python>`_ under the hood to communicate with the app search instance. So if needed, you can access the app search instance directly and use the functionality of the official elastic app search `client <https://github.com/elastic/app-search-python#usage>`_. Example below.

.. code-block:: python

    from django_elastic_appsearch.clients import get_api_v1_client

    client = get_api_v1_client()
    client.search('cars', 'Toyota Corolla', {})

Contributing
------------

Contributors are welcome!

* Prior to opening a pull request, please create an issue to discuss the change/feature you've written/thinking of writing.

* Please write simple code and concise documentation, when appropriate.

* Please write test cases to cover the code you've written, where possible.

Running Tests
-------------

Does the code actually work?

::

    $ pipenv install --dev
    $ pipenv shell
    (django_elastic_appsearch) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
