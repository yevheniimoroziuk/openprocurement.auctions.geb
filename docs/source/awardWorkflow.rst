.. _awardWorkflow: 

##############
Award Workflow
##############

Procedure Workflow for 1 Submitted Bid
======================================

Award Section
-------------

.. graphviz::

    digraph G {
        subgraph cluster_1 {
            node [style=filled, fillcolor=seashell2];
            edge[style=dashed,  arrowhead="vee", label="*"];
            "pending" -> "active";
            node [style=filled, fillcolor=white];
            edge[style=dashed,  arrowhead="vee",  label="~~", constraint=false];
            "pending" -> "unsuccessful";
            edge[style=solid,  arrowhead="vee",  label="**", constraint=false];
            "pending" -> "unsuccessful";
            edge[style=solid,  arrowhead="vee", label="~", constraint=false];
            "active" -> "unsuccessful"; 
            label = "Awarding Process";
            color=white
            {rank=same; "active" "unsuccessful"}
        }
    }

Legend
""""""

 \* admission protocol is downloaded and award is switched to `active` by the organizer.
 
 \*\* organizer has decided to disqualify the bidder. The approptiate document is downloaded and award is manually switched to `unsuccessful`.

 \~\~ admission protocol is not downloaded and award is not switched to `pending` by the organizer in time.

 \~ contract is switched to `cancelled` and award is manually switched to `unsuccessful`.

Roles
"""""

:Chronograph: solid

:Organizer:  dashed


Contract Section
----------------

.. graphviz::

    digraph G {
        subgraph cluster_1 {
            node [style=filled, fillcolor=seashell2];
            edge[style=dashed,  arrowhead="vee", label="*"];
            "pending" -> "acive";
            label = "Contract Workflow";
            color=white
        }
        edge[style=dashed,  arrowhead="vee",  label="**"];
        "pending" -> "cancelled";
    }

Legend
""""""

 \* document was downloaded to contract. The contract itself was successfully activated by the organizer.

 \*\* there was no document uploaded. The organizer refused to activate the contract.

Roles
"""""

:Chronograph: solid

:Organizer:  dashed

1. The procedure receives `active.qualification` status. 

2. The award initially receives `pending` status. The awarding process enters  the `verificationPeriod` phase. If the actions needed are not completed, the award auctomatically receives `unsuccessful` status, so that the procedure will be switched to `unsuccessful` as well.

    2.1 If the organizer decides to disqualify the bidder, a document (`documentType: rejectionProtocol` or `act`) has to be downloaded first and the award has to be manually switched to `unsuccessful` then. The procedure will be given `unsuccessful` status this way.

3. When the conditions are met, the process enters the `verificationPeriod`. During this term the organizer uploads the protocol (`documentType: auctionProtocol`) first and manually switches award to `active` status then. Simultaneously the awarding process enters the signingPeriod phase and the procedure receives `active.awarded` status.

    3.1 If the organizer decides to disqualify the bidder, a document (`documentType: rejectionProtocol` or `act`) has to be downloaded first and the award has to be manually switched to `unsuccessful` then.

4. It is then when the qualification procedure enters the `signingPeriod` stage. The contract of the qualifying bid initially receives a `pending` status. Within this time, the organizer should upload the document (`documentType: contractSigned`) in the system and manually switch contract to `active` status in order to successfully finish the qualification procedure. 

    4.1 For the bidder to be disqualified a document (`documentType: rejectionProtocol` or `act`) has to be downloaded first and the contract has to be manually switched to `cancelled` by the organizer then. As long as such an action is done, award status will receive `unsuccessful`.

Notes
=====

1. The auto-generated period duration does not influence the actions which can be done.

2. The organizer can disqualify the award at any stage of the awarding process up to the moment, when a document with the `documentType: contractSigned` has been downloaded. 

Statuses
========

:pending:
   :`Award`: Awaiting for the protocol to be uploaded and confirmed by the organizer. The valid bidder is able to submit the protocol as well, although it is not sufficient to move to the next status.

   :`Contract`: Awaiting for the contract to be signed (uploaded and activated in the system by the organizer).

:active:
    :`Award`: Auction protocol (`documentType: auctionProtocol`) was downloaded so that the award could be switched to `active` by the organizer.

    :`Contract`: The document (`documentType: contractSigned`) was downloaded  so that the status of the contract object could be switched to `active` by the organizer.

:unsuccessful:
    Terminal status of award. Rejection protocol or act (`documentType: rejectionProtocol/act`) was downloaded so that the award could be switched to `unsuccessful` by the organizer. Or when the contract becomes status `cancelled`, the status of the award will be `unsuccessful`.

:cancelled:
    Terminal status of contract. Rejection protocol or act (`documentType: rejectionProtocol/act`) was downloaded so that the contract could be switched to `cancelled` by the organizer.
