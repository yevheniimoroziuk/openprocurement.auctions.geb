.. _bid:

Bid
===

Schema
------

:id:
    uuid, auto-generated, read-only

    Internal identifier of bid.

:tenderers:
    Array of :ref:`Organization` objects, required

:date:
    string, :ref:`date`, auto-generated, read-only
    
    Date when bid has been submitted.

:owner:
    string, auto-generated, read-only

    Broker_id of the platform from which the procedure has been created

:value:
    :ref:`Value`, required

    Validation rules:

    * `amount` should be less than `Auction.value.amout`
    * `currency` should either be absent or match `Auction.value.currency`
    * `valueAddedTaxIncluded` should either be absent or match `Auction.value.valueAddedTaxIncluded`

:status:
    string, required

    Possible values are:

    * `draft`
    * `pending`
    * `active`
    * `unsuccessful`

:documents:
    Array of :ref:`Document`, optional

    All documents needed.

:participationUrl:
    url, auto-generated, read-only

    A web address for participation in auction.

:qualified:
    bool, required

    The field fills owner. Сonfirms that the participant fulfilled all conditions.

:bidNumber:
    integer, optional

    Order number of the bidder.
