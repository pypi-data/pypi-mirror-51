==============
collective.gnd
==============

Plone addon which provides a `GND ID <https://www.wikidata.org/wiki/Property:P227>`_ resolver and a `BEACON <http://gbv.github.io/beaconspec/>`_ API.

Features
--------

- GND ID resolver: ``/resolvegnd/08151111``
- GND ID Behavior, which provides a ``gnd_id`` field
- Provides a ``gnd_id`` index
- BEACON API (BEACON List): /beacon-gnd.txt


Installation
------------

Install collective.gnd by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.gnd


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.gnd/issues
- Source Code: https://github.com/collective/collective.gnd


License
-------

The project is licensed under the GPLv2.
