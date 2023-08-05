.. image:: https://secure.travis-ci.org/collective/collective.edtf_behavior.png?branch=master
    :target: http://travis-ci.org/collective/collective.edtf_behavior

.. image:: https://coveralls.io/repos/github/collective/collective.edtf_behavior/badge.svg?branch=master
    :target: https://coveralls.io/github/collective/collective.edtf_behavior?branch=master
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/l/collective.edtf_behavior.svg
    :target: https://pypi.python.org/pypi/collective.edtf_behavior/
    :alt: License

.. image:: https://badges.gitter.im/collective/collective.edtf_behavior.svg
   :alt: Join the chat at https://gitter.im/collective/collective.edtf_behavior
   :target: https://gitter.im/collective/collective.edtf_behavior?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


========================
collective.edtf_behavior
========================

A Plone behavior which provides a `EDTF <http://www.loc.gov/standards/datetime/edtf.html>`_  Date field and some indexes to search and sort on complex and historic dates.

Note: the current implementation of the used library `python-edtf <https://pypi.org/project/edtf/>`_ , still uses an earlier draft of the standard: http://www.loc.gov/standards/datetime/pre-submission.html


Features
--------

- Allows unspecific dates or date intervals: "1989-11" or "1989-11~" or "1989-11-01/1989-11-30"
- Seasons: 2001-21  >> Spring, 2001
- old dates like 03.08.1492
- Search indexes: date_earliest and date_latest
- Sort indexes: date_sort_ascending and date_sort_descending


Installation
------------

Install collective.edtf_behavior by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.edtf_behavior


and then running ``bin/buildout``

After you activated the add-on in the Plone Add-ons section, you can Enable this behavior on any Dexterity based content type.

Querying
--------

.. code-block:: python

        from plone import api

find any document which earliest date is 06.02.1920 or later.

.. code-block:: python

        results = api.content.find(
            portal_type='Document',
            date_earliest={
                'query': datetime.date(1920, 2, 6),
                'range': 'min',
            },
        )

find any document which latest date is 11.11.1711 or earlier.

.. code-block:: python

        results = api.content.find(
            portal_type='Document',
            date_latest={
                'query': datetime.date(1711, 11, 11),
                'range': 'max',
            },
        )

This package provides a `DateRangeInRangeIndex <https://pypi.org/project/Products.DateRangeInRangeIndex/>`_  named ``edtf_start_end_range``.

find all documents that fall at least with one start/end date of there interval into the range:

.. code-block:: python

        results = api.content.find(
            portal_type='Document',
            edtf_start_end_range={
                'start': datetime.date(1711, 11, 11),
                'end':   datetime.date(1920, 2, 6),
            },
        )

For more examples how to query the indexes, have a look at the `tests <https://github.com/collective/collective.edtf_behavior/tree/master/src/collective/edtf_behavior/tests>`_ .


Extending it
------------

One could improve indexing by using a DateRangeIndex, like the effectiveRange index in Plone if needed.

.. code-block:: xml

    <!-- Example of a DateRangeIndex like the effectiveRange index in Plone -->
    <index name="edtf_date_range" meta_type="DateRangeIndex"
      since_field="date_earliest" until_field="date_latest" />


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.edtf_behavior/issues
- Source Code: https://github.com/collective/collective.edtf_behavior


Support
-------

If you are having issues, please let us know.
You can reach us on Gitter.


License
-------

The project is licensed under the GPLv2.
