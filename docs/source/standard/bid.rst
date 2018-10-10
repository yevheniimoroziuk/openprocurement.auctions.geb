.. _bid:

Bid
===

Schema
------

:tenderers:
    Array of :ref:`Organization` objects, required

:date:
    string, :ref:`date`, auto-generated
    
    Date when bid has been submitted.

:id:
    uuid, auto-generated

    Internal identifier of bid.

:status:
    string, required

    Possible values are:

    * `draft`
    * `pending`
    * `active`
    * `deleted`
    * `unsuccessful`
    
:value:
    :ref:`Value`, required

    Validation rules:

    * `amount` should be less than `Auction.value.amout`
    * `currency` should either be absent or match `Auction.value.currency`
    * `valueAddedTaxIncluded` should either be absentuntitled or match `Auction.value.valueAddedTaxIncluded`

:documents:
    Array of :ref:`Document`, optional

    All documents needed.

:participationUrl:
    URL, auto-generated

    A web address for participation in auction.

:qualified:
    bool, required

    The field fills owner. Сonfirms that the participant fulfilled all conditions.

:eligible:
    bool, optional 

    Confirms compliance of eligibility criteria set by the customer in the tendering documents. CDB accepts only true value.

:bidNumber:
    integer, required

    The field fills owner. Number of participant in the auction.
