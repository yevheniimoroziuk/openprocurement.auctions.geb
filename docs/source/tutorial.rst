.. _tutorial:

Tutorial
========

create
------

Let's create some auction:

.. include:: tutorial/create_auction.http
    :code:


Success! Now we can see that new object has been created. Response code is `201`
and `Location` response header reports the location of the created object.  The
body of response reveals the information about the created auction: its internal
`id` (that matches the `Location` segment), its official `auctionID` and
`dateModified` datestamp stating the moment in time when auction has been last
modified. Pay attention to the `procurementMethodType`. Note that auction is
created with `draft` status.

draft
-----

get
^^^

After the creation of the auction we can get it

.. include:: tutorial/get_draft_auction.http
    :code:

two-phase commit
^^^^^^^^^^^^^^^^

In order to activate the auction, we must make a two-phase commit

.. include:: tutorial/phase_commit.http
    :code:

We can see what new fields were generated in auction:

rectificationPeriod
        it lasts 2 working days (non-working days).
        During this period, you can change some fields
tenderPeriod
        this period ends at 8:00 pm 3 business days before the auction starts.
        During this period, it is allowed to add documents, work with bids, work with questions
enquiryPeriod
        this period ends at 8:00 pm 1 business days before the auction starts.
        During this period, it is allowed to add documents, work with bids, work with questions

active.rectification
--------------------

auctions
^^^^^^^^

change fields
"""""""""""""

After the auction is activated, the auction goes into `active.rectification` status
In this period we can change next fields:

- title
- description
- tenderAttempts
- lotIdentifier
- value
- minimalStep
- guarantee
- items
- budgetSpent
- registrationFee
- procuringEntity
- lotHolder
- bankAccount
- contractTerms

Example:

.. include:: tutorial/active_rectification_change_title.http
    :code:

auction documents

.. _adding auction documents:

auctions documents
^^^^^^^^^^^^^^^^^^

add
"""

Example:

.. include:: tutorial/active_rectification_add_document.http
    :code:


active.tendering
----------------

In active.tendering we can:

- adding :ref:`adding auction documents`
- work with questions
- work with bids

.. _work with questions:

work with questions
^^^^^^^^^^^^^^^^^^^

ask
"""

After the auction has passed to the `active.tendering` status, we can ask questions:

.. include:: tutorial/active_tendering_add_question.http
    :code:

answer
""""""

if we have any `questions` we can answer them:

.. include:: tutorial/active_tendering_answer_question.http
    :code:

We can see the `answer` field appeared

.. _work with bids:

work with bids
^^^^^^^^^^^^^^

add
"""

In `active.tendering` status, we can add bids:

.. include:: tutorial/active_tendering_add_bid.http
    :code:

get
"""

Get the bid:

.. include:: tutorial/active_tendering_get_bid.http
    :code:

activate
""""""""

As we can see the bid is in draft status.
In order to `activate bid` we must change status to `pending`:

.. include:: tutorial/active_tendering_activate_bid.http
    :code:

We can see that the following fields have been generated:

- date
- id
- owner
- qualified: false

make active status
""""""""""""""""""

When a bit in `pending` status it does not mean a fully active bit.
In order to set `active` status we must

- attach document with `documentType: eligibilityDocuments`
- patch bid, set `qualified: true`
- patch bid, set `bidNumber - integer`
- patch bid, set `status - active`

Performing the last three actions should be done as separate PATCHs, or the one PATCH


Let`s try to completely activate bid

Attach document with `documentType: eligibilityDocuments`:

.. include:: tutorial/active_tendering_bid_attach_document.http
    :code:

Patch with required data for completely activate bid:

.. include:: tutorial/active_tendering_bid_make_active_status.http
    :code:

Now we can see completely activated bid:

.. include:: tutorial/active_tendering_bid_get_active_status.http
    :code:

We can delete bid:

.. include:: tutorial/active_tendering_delete_bid.http
    :code:

active.enquiry
--------------
In active.enquiry we can:

- adding :ref:`adding auction documents`
- :ref:`work with questions`
- :ref:`work with bids`
        - allowed:
                - pending-> active
                - pending-> deleted
                - active-> deleted
        - is prohibited:
                - create a draft

active.auction
--------------
After auction is scheduled anybody can visit it to watch. The auction can be reached at `Auction.auctionUrl`:

.. include:: tutorial/active_auction_get_procedure.http
    :code:
