.. _cancellation:

Cancellation
============

Schema
------

:id:
    uuid, auto-generated

:reason:
    string, multilingual, required

    The reason, why auction is being cancelled.

:status:
    string

    Possible values are:
     :`pending`:
       Default. The request is being prepared.
     :`active`:
       Cancellation activated.

:documents:
    List of :ref:`Document` objects

    Documents accompanying the Cancellation: Protocol of Auction Committee
    with decision to cancel the Auction.

:date:
    string, :ref:`date`

    Cancellation date.

:cancellationOf:
    string

    Possible values are:

    * `auction`