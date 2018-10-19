.. include:: defs.hrst

.. index:: Period, startDate, endDate
.. _period:

Period
======

Schema
------

:startDate:
    :ref:`date`

    |ocdsDescription|
    The start date for the period.

:endDate:
    :ref:`date`

    |ocdsDescription|
    The end date for the period.

`startDate` should always precede `endDate`.

.. _Date:

Date
====

Date/time in `ISO 8601 <http://en.wikipedia.org/wiki/ISO_8601>`_.

.. index:: Value, Currency, VAT
.. _value:

Value
=====

Schema
------

:amount:
    float, required

    |ocdsDescription|
    Amount as a number.

    Should be positive.

:currency:
    string, required

    |ocdsDescription|
    The currency in 3-letter ISO 4217 format.

:valueAddedTaxIncluded:
    bool, optional

    The default value is ``true``.

.. index:: Revision, Change Tracking

.. _guarantee:

Guarantee
=========

Schema
------

:amount:
    float, required

    |ocdsDescription|
    Amount as a number.

    Should be positive.

:currency:
    string, required

    |ocdsDescription|
    The currency in 3-letter ISO 4217 format. `UAH` by default.
