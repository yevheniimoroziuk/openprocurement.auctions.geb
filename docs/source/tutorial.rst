.. _tutorial:

Tutorial
========

create procedure
----------------

Let’s create some procedure:

.. include:: tutorial/create_auction.http
    :code:


Success! Now we can see that new object has been created. Response code is `201`
and `Location` response header reports the location of the created object.  The
body of response reveals the information about the created auction: its internal
`id` (that matches the `Location` segment), its official `auctionID` and
`dateModified` datestamp stating the moment in time when auction has been last
modified. Pay attention to the `procurementMethodType`. Note that auction is
created with `draft` status.

status: draft
-------------

get procedure
^^^^^^^^^^^^^

You can GET the auction as long as it's been created

.. include:: tutorial/get_draft_auction.http
    :code:

two-phase commit
^^^^^^^^^^^^^^^^

For the procedure to be activated you should apply
a two-phase commit (manually switch procedure to `active.rectification` status)

.. include:: tutorial/phase_commit.http
    :code:

We can see what new fields were generated in auction:

rectificationPeriod
        it lasts for 2 days.
        During this period, you can change some fields
tenderPeriod
        this period ends at 8:00 pm 3 business days before the auction starts.
        During this period, it is allowed to add documents, work with bids & questions
enquiryPeriod
        this period ends at 8:00 pm the days before the auction starts
        During this period, it is allowed to add documents, work with bids & questions

status: active.rectification
----------------------------

auctions
^^^^^^^^

change fields
"""""""""""""

After the procedure is activated, it receives `active.rectification` status.
During this term you can edit the next data:

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


.. _add auction documents:

auctions documents
^^^^^^^^^^^^^^^^^^

add document
""""""""""""

Example:

.. include:: tutorial/active_rectification_add_document.http
    :code:


status: active.tendering
------------------------

In active.tendering we can:

- add :ref:`add auction documents`
- work with questions
- work with bids

.. _work with questions:

work with questions
^^^^^^^^^^^^^^^^^^^

ask question
""""""""""""

Bidders can ask questions within the `enquiryPeriod`:

.. include:: tutorial/active_tendering_add_question.http
    :code:

answer question
"""""""""""""""

The Organizer can provide the answer:

.. include:: tutorial/active_tendering_answer_question.http
    :code:

We can see the `answer` field appeared

.. _work with bids:

work with bids
^^^^^^^^^^^^^^

add bid
"""""""

In `active.tendering` status, we can add bids:

.. include:: tutorial/active_tendering_add_bid.http
    :code:

get bid
"""""""

You can also GET the created bid:

.. include:: tutorial/active_tendering_get_bid.http
    :code:

activate
""""""""

The bid is created in draft status. Use `pending` status for its activation:

.. include:: tutorial/active_tendering_activate_bid.http
    :code:

We can see that the following fields have been generated:

- date
- id
- owner
- qualified: false

make active status
""""""""""""""""""

As long as a pre-qualification process has been performed out of the system,
bid owner should add the next data

- attach document with `documentType: eligibilityDocuments`
- patch bid, set `qualified: true`
- patch bid, set `bidNumber - integer`
- patch bid, set `status - active`

The last 3 actions can be performed either using separate PATCHs, or applying the one


Let's complete bid activation

Attach document with `documentType: eligibilityDocuments`:

.. include:: tutorial/active_tendering_bid_attach_document.http
    :code:

Patch with required data for a complete bid activation:

.. include:: tutorial/active_tendering_bid_make_active_status.http
    :code:

Now we can see completely activated bid:

.. include:: tutorial/active_tendering_bid_get_active_status.http
    :code:

We can delete bid:

.. include:: tutorial/active_tendering_delete_bid.http
    :code:

status: active.enquiry
----------------------
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

status: active.auction
----------------------
After auction is scheduled anybody can visit it to watch. The auction can be reached at `Auction.auctionUrl`:

.. include:: tutorial/active_auction_auction_url.http
    :code:

We can see what `auctionUrl` were generated in procedure

And bidders can find out their participation URLs via their bids:

.. include:: tutorial/active_auction_participation_urls.http
    :code:
We can see what `participationUrl` were generated in bid
