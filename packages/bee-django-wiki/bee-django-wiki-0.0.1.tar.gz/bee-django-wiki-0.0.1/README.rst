============
wiki
============

Quick start
-----------

1. Add "message" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'bee_django_wiki.apps.BeeDjangoMessageConfig',
    )

2. Include the crm URLconf in your project urls.py like this::

    from django.conf.urls import include, url
    ...
    url(r'^wiki/', include('bee_django_wiki.urls')),

3.settings.py like this::

    WIKI_TOPIC_UPLOAD_MAXSIZE = 2 #option

3. Run `python manage.py makemigrations`,`python manage.py migrate` to create the crm models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a message (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/wiki/ to participate in the message.
