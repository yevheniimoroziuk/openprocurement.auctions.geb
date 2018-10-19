.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Auction, Auction
.. _auction:

Auction
=======

Schema
------

:id:
  uuid, auto-generated, read-only

  Internal id of procedure.
  
:auctionID:
  string, auto-generated, read-only

  The auction identifier to refer to in "paper" documentation. 

  |ocdsDescription|
  It is included to make the flattened data structure more convenient.

:date:
  :ref:`Date`, auto-generated, read-only

  The date of the procedure creation/undoing.

:owner:
  string, auto-generated, read-only
  
  Broker_id of the platform from which the procedure has been created
 
:lotIdentifier:
  string, required

  The identifier of a lot, which is to be privatized, within the Registry.

:title:
    string, multilingual, required
    
    * Ukrainian by default (required) - Ukrainian title
    
    * ``title_en`` (English) - English title
    
    * ``title_ru`` (Russian) - Russian title
    
    Oprionally can be mentioned in English/Russian.

  The name of the auction, displayed in listings. 
 
:description:
    string, required, multilingual
    
    |ocdsDescription|
    A description of the goods, services to be provided.
    
    * Ukrainian by default - Ukrainian decription
    
    * ``decription_en`` (English) - English decription
    
    * ``decription_ru`` (Russian) - Russian decription


:tenderAttempts:
  integer, optional

  The number which represents what time procedure with a current lot takes place [1;10].

:minNumberOfQualifiedBids:
  integer, optional

  Number of submitted bids for the process to become successful. The default value is 2.

:procurementMethod:
  string, auto-generated, read-only

  Purchase method. The only value is “open”.
  
:procurementMethodType:
  string, required
  
  Type of the procedure within the auction announcement. The given value is landLease. 

:procurementMethodDetails:
  string, optional
  
  Parameter that accelerates auction periods. Set quick, accelerator=1440 as text value for procurementMethodDetails for the time frames to be reduced in 1440 times.

:submissionMethod:
  string, auto-generated, read-only

  The given value is `electronicAuction`.

:submissionMethodDetails:
  string, optional

  Parameter that works only with mode = “test” and speeds up auction start date.

:lotHolder:
   :ref:`Organization`, required

   The entity whom the lot was used to be owned by.

:procuringEntity:
  :ref:`ProcuringEntity`, required

  Organization conducting the auction.

  |ocdsDescription|
  The entity managing the procurement, which may be different from the buyer who is paying / using the items being procured.

:auctionParameters:
  :ref:`Auction_Parameters`, auto-generated, read-only

  The parameters that indicates the major specifications of the procedure.

:contractTerms:
  :ref:`contractTerms`, required

  The parameters that indicates the major specifications of the contract.

:budgetSpent:
  :ref:`value`, required

  The amount of expenses incurred for the preparation of a lot for the sale, organization and conduct of land auction, subject to compensation by the winner of land tenders.

:value:
  :ref:`value`, required

  Total available budget of the 1st auction. Bids lower than ``value`` will be rejected.

  |ocdsDescription|
  The total estimated value of the procurement.

:minimalStep:
  :ref:`value`, required

  Auction step (increment). 
  
:guarantee:
  :ref:`Guarantee`, required

  The assumption of responsibility for payment of performance of some obligation if the liable party fails to perform to expectations.

:registrationFee:
  :ref:`Guarantee`, required

  The sum of money required to enroll on an official register.

:bankAccount:
  :ref:`Bank_Account`, optional

  An array that contains parts that uniquely identify a bank account and are used for making or receiving a payment.

:items:
  Array of :ref:`Items` objects, required

  List that contains single item being sold.

  |ocdsDescription|
  The goods and services to be purchased, broken into line items wherever possible. Items should not be duplicated, but a quantity of 2 specified instead.

:documents:
  Array of :ref:`Documents` objects, optional

  |ocdsDescription|
  All documents and attachments related to the auction.

:dateModified:
  :ref:`Date`, auto-generated, read-only

  |ocdsDescription|
  Date when the auction was last modified

:questions:
  Array of :ref:`question` objects, optional

  Questions to `procuringEntity` and answers to them.

:bids:
  Array of :ref:`bid` objects, optional (required for the process to be succsessful)
  
  A list of all bids placed in the auction with information about participants, their proposals and other qualification documentation.

  |ocdsDescription|
  A list of all the companies who entered submissions for the auction.

:awards:
  Array of :ref:`award` objects

  All qualifications (disqualifications and awards).

:awardCriteria:
  string, auto-generated, read-only

  The given value is `highestCost`.

:contracts:
  Array of :ref:`Contract` objects

  |ocdsDescription|
  Information on contracts signed as part of a process.

:auctionUrl:
  url, auto-generated, read-only

  A web address where auction is accessible for view.

:status:
  string, required

+-------------------------+--------------------------------------+
|        Status           |            Description               |
+=========================+======================================+
| `draft`                 | draft of procedure                   |
+-------------------------+--------------------------------------+
| `active.rectification`  | period when owner can edit procedure |
+-------------------------+--------------------------------------+
| `active.tendering`      | tendering period (tendering)         |
+-------------------------+--------------------------------------+
| `active.enquiry`        | status after tendering               |
+-------------------------+--------------------------------------+
| `active.auction`        | auction period (auction)             |
+-------------------------+--------------------------------------+
| `active.qualification`  | winner qualification (qualification) |
+-------------------------+--------------------------------------+
| `active.awarded`        | contract signing                     |
+-------------------------+--------------------------------------+
| `unsuccessful`          | unsuccessful auction (unsuccessful)  |
+-------------------------+--------------------------------------+
| `complete`              | complete auction (complete)          | 
+-------------------------+--------------------------------------+
| `cancelled`             | cancelled auction (cancelled)        |
+-------------------------+--------------------------------------+

:rectificationPeriod:
  :ref:`period`, auto-generated, read-only

  Period when owner can edit the procedure.

:enquiryPeriod:
  :ref:`period`, auto-generated, read-only

  Period when questions are allowed.

  |ocdsDescription|
  The period during which enquiries may be made and will be answered.

:tenderPeriod:
  :ref:`period`, auto-generated, read-only

  Period when bids can be submitted.

  |ocdsDescription|
  The period when the auction is open for submissions. The end date is the closing date for auction submissions.

:auctionPeriod:
  :ref:`period`, auto-generated, read-only (required for ``auctionPeriod.startDate``)

  Period when Auction is conducted.

:awardPeriod:
  :ref:`period`, auto-generated, read-only

  Awarding process period.

  |ocdsDescription|
  The date or period on which an award is anticipated to be made.

:mode: 
  string, optional

  The additional parameter with a value `test`.

.. _Auction_Parameters:
  
Auction Parameters
==================

Schema
------

:type:  
    string, auto-generated, read-only

    Type of the auction. Given value: `texas`

Bank Account
============

Schema
------

:description:
  string, multilingual, optional

    * Ukrainian by default - Ukrainian decription
    
    * ``decription_en`` (English) - English decription
    
    * ``decription_ru`` (Russian) - Russian decription

  Additional information that has to be noted from the Organizer point.
  
:bankName:  
  string, required

  Name of the bank.
  
:accountIdentification:
  Array of :ref:`classification`, required

  Major data on the account details of the state entity selling a lot, to facilitate payments at the end of the process.

  Most frequently used are:

  * 'UA-EDR';
  * 'UA-MFO';
  * 'accountNumber'.

.. _contractTerms:

Contract Terms
==============

Schema
------

:type:
  string, required

  Type of the contract. The only value is `lease`.

:leaseTerms:
  :ref:`leaseTerms`, required

  Additional informations about speciality of contract.

.. _leaseTerms:

Lease Terms
===========

Schema
------

:leaseDuration:
  ISO Durations, required

  Duration of the lease.
