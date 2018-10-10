Overview
========

openprocurement.auctions.geb contains documentaion regarding open ascending price auctions within the Lease of Land process.

Type of the given procedure:

* landLease

Features
--------



Conventions
-----------

API accepts `JSON <http://json.org/>`_ or form-encoded content in
requests.  It returns JSON content in all of its responses, including
errors.  Only the UTF-8 character encoding is supported for both requests
and responses.

All API POST and PUT requests expect a top-level object with a single
element in it named `data`.  Successful responses will mirror this format. 
The data element should itself be an object, containing the parameters for
the request.  In the case of creating a new auction, these are the fields we
want to set on the auction itself.

If the request was successful, we will get a response code of `201`
indicating the object was created.  That response will have a data field at
its top level, which will contain complete information on the new auction,
including its ID.

If something went wrong during the request, we'll get a different status
code and the JSON returned will have an `errors` field at the top level
containing a list of problems.  We look at the first one and print out its
message.

Project status
--------------

The project has pre alpha status.

The source repository for this project is on GitHub: https://github.com/openprocurement/openprocurement.auctions.geb

You can leave feedback by raising a new issue on the `issue tracker
<https://github.com/openprocurement/openprocurement.auctions.geb/issues>`_ (GitHub
registration necessary).

Documentation of related packages
---------------------------------

* `OpenProcurement API <http://api-docs.openprocurement.org/en/latest/>`_
* `Assets Registry <http://assetsbounce.api-docs.registry.ea2.openprocurement.io/en/latest/>`_
* `Lots Registry <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/>`_
* `Contracting <http://ceasefire.api-docs.ea2.openprocurement.io/en/latest/standard/contract.html>`_

API stability
-------------

API is relatively stable. The changes in the API are communicated via `Open Procurement API
<https://groups.google.com/group/open-procurement-api>`_ maillist and ProZorro.Sale Slack chats.

Change log
----------

0.1
~~~

Released: not released

Next steps
----------
You might find it helpful to look at the :ref:`tutorial`.
