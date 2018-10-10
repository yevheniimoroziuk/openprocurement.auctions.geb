.. index:: Question, Answer, Author
.. _question:

Question
========

Schema
------

:id:
    uuid, auto-generated, read-only

    Internal identifier of the object within an array.

:author:
    :ref:`Organization`, optional

    Who is asking a question (contactPoint - person, identification - organization that person represents).

:title:
    string, required

    Title of the question.

:description:
    string, optional

    Description of the question.

:date:
    :ref:`date`, auto-generated, read-only

    Date of posting.

:answer:
    string, optional

    Answer for the question.

:questionOf:
    string, required

    Possible values are:

    * `tender`
    * `item`

:relatedItem:
    uuid, optional

    Internal ID of related :ref:`item`.
