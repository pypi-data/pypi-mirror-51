|PyPI version| |Build status| |Dependency Status|

Niddel Magnet v2 API Python SDK
===============================

A simple client that allows idiomatic access to the `Niddel Magnet v2
REST API <https://api.niddel.com/v2>`__. Uses the wonderful
`requests <http://docs.python-requests.org/>`__ package to perform the
requests.

Release history:
https://github.com/Niddel/magnet-api2-sdk-python/releases

Configuring Credentials
-----------------------

There are a couple of ways to let the ``Connection`` object know which
API key to use. The simplest one is to pass one explicitly to its
constructor:

.. code:: python

    from magnetsdk2 import Connection

    conn = Connection(api_key="my secret API key")

If an explicit API key is not provided, the ``Connection`` constructor
will look for one first in the ``MAGNETSDK_API_KEY`` environment
variable and failing that in the ``default`` profile of the
configuration file.

You can add different API keys to a configuration file with different
profiles by creating a file called ``.magnetsdk/config`` under the
current user's home directory. It is a basic Python configuration file
that looks like the following:

::

    [default]
    api_key=my secret api key

    [profile2]
    api_key=another secret api key

So in this case you could create a connection to use either API key as
follows:

.. code:: python

    from magnetsdk2 import Connection

    conn_default = Connection()                     # uses default profile
    conn_profile2 = Connection(profile='profile2')  # use profile2 explicitly

Using the SDK
-------------

It's as simple as creating a ``Connection`` object and using it to
perform queries. This small example shows you how to print out all of
the organizations the configured API key has access to.

.. code:: python

    import json
    from magnetsdk2 import Connection

    conn = Connection()
    for org in conn.iter_organizations():
        print(json.dumps(org, indent=4))

Downloading Only New Alerts
---------------------------

A common scenario for using the SDK is downloading only new alerts over
time, typically to feed an integration with a 3rd party SIEM or
ticketing system. In order to implement this, the concept of a
persistent iterator that saves its state on a JSON file is provided in
the SDK:

.. code:: python

    from magnetsdk2 import Connection
    from magnetsdk2.iterator import FilePersistentAlertIterator

    conn = Connection()
    # replace xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx with a valid organization ID 
    alert_iterator = FilePersistentAlertIterator('persistence.json', conn, 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
    for alert in alert_iterator:
        try:
            # try to process alert in some way
            print(alert)
        except:
            alert_iterator.load()   # on failure, reload iterator so last alert doesn't count as processed
        else:
            alert_iterator.save()   # on success, save iterator so last alert counts as processed

If you run this same code multiple times, it should ever only output
alerts it hasn't processed before, provided file ``persistence.json`` is
not tampered with and remains available for reading and writing.

You save the current state of the iterator with the ``save`` method. If
you tried to process an alert and failed, you can simply not save the
iterator and reload the previous consistent state from disk using the
``load`` method.

Though the provided implementation saves the data to a JSON file, it is
easy to add other means of persistence by creating subclasses of
``magnetsdk2.iterator.AbstractPersistentAlertIterator`` that implement
the abstract ``_save`` and ``_load`` methods.

Command-line Utility
--------------------

Starting with version 1.2.0, the package installs a ``niddel``
command-line utility which can be used to perform most of the same
functionalities available on the SDK. First install the package:

.. code:: bash

    $ pip install magnetsdk2

Then, you can see that a ``--profile`` option can be provided to select
an alternative API key from ``~/.magnetsdk/config``, as described
previously:

.. code:: bash

    $ niddel -h
    usage: niddel [-h] [-p PROFILE] [-i] [-v] [-o OUTFILE]
                  {me,organizations,alerts,logs} ...

    Command-line utility to interact with the Niddel Magnet v2 API (v1.4.1)

    positional arguments:
      {me,organizations,alerts,logs}
        me                  display API key owner information
        organizations       list basic organization information
        alerts              list an organization's alerts
        logs                upload, download or list log files

    optional arguments:
      -h, --help            show this help message and exit
      -p PROFILE, --profile PROFILE
                            which profile (from ~/.magnetsdk/config) to obtain API
                            key from
      -i, --indent          indent JSON output
      -v, --verbose         set verbose mode
      -o OUTFILE, --outfile OUTFILE
                            destination file to write to, if exists will be
                            overwritten

You can even use a persistent alert iterator by providing a file name
with ``--persist`` when listing alerts:

.. code:: bash

    $ niddel alerts -h
    usage: niddel alerts [-h] [--start START] [-p PERSIST] [-f {json,cef}]
                         organization

    list an organization's alerts

    positional arguments:
      organization          ID of the organization

    optional arguments:
      -h, --help            show this help message and exit
      --start START         initial batch date to process in YYYY-MM-DD format
      --cursor CURSOR       latest cursor returned setting the initial batch of alerts
      -p PERSIST, --persist PERSIST
                            file to store persistent state data, to ensure only
                            alerts that haven't been seen before are part of the
                            output
      -f {json,cef}, --format {json,cef}
                            format in which to output alerts

Keep in mind that the persistence state is only saved immediately before
the command exits, after all unprocessed alerts have been printed to
stdout. So if the CLI utility is interrupted or if an exception occurs
mid-processing, no state is saved and any alerts output in this failed
execution are not considered processed.

The default output format for alerts is JSON, but if you provide
``--format cef`` then the `ArcSight Common Event
Format <https://community.saas.hpe.com/t5/ArcSight-Connectors/ArcSight-Common-Event-Format-CEF-Guide/ta-p/1589306>`__
will be used instead.

.. |PyPI version| image:: https://badge.fury.io/py/magnetsdk2.svg
   :target: https://badge.fury.io/py/magnetsdk2
.. |Build status| image:: https://ci.appveyor.com/api/projects/status/7k25x3lphcxagb7t/branch/master?svg=true
   :target: https://ci.appveyor.com/project/asieira/magnet-api2-sdk-python/branch/master
.. |Dependency Status| image:: https://dependencyci.com/github/Niddel/magnet-api2-sdk-python/badge
   :target: https://dependencyci.com/github/Niddel/magnet-api2-sdk-python
