=============
weblogtools
=============

Weblogtools is a simple Django app to log http request to database, in order to have a nice interface to check the input / output data with external service.

Quick start
-------------

1. Add "weblogtools" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'weblogtools',
    ]

2. Include the weblogtools URLconf in your project urls.py like this::

    path('weblogtools/', include('weblogtools.urls')),

3. Run `python manage.py migrate` to create the weblogtools models.

4. now you can use weblogtools like belows. more see the weblogtools package source code::

    with weblogtools.biz.TimeIt() as timeit:
        res = requests.post(url, json=payload)
    weblogtools.biz.http_log_from_response('upload_case', res, timeit.duration)
