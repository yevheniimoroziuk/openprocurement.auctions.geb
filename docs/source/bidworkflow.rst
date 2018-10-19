.. _bid_workflow: 

############
Bid Workflow
############

.. graphviz::

    digraph G {
        subgraph cluster_2 {
            node [style=filled, fillcolor=seashell2];
            edge[style=dashed];
            "draft" -> "pending" [color="0.7777 1.0000 0.5020"];
        color=white;
        }

        subgraph cluster_4 {
            node [style=filled, fillcolor=seashell2];
            edge[style=dashed, dir="forward"];
            "pending" -> "active" [color="0.7777 1.0000 0.5020"];  
        color=white;
        }

        subgraph cluster_3 {
            node [style=filled, fillcolor=white];
            edge[style=solid];
            "pending" -> "unsuccessful" [color="0.0000 0.0000 0.3882"];
        color=white;
        }
    }

Roles
"""""

:Chronograph: solid

:Organizer:  dashed