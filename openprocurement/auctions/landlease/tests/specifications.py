# Definition of the scheme required in accordance with the specifications, change it ONLY in case of changes to the specification

REQUIRED_SCHEME_DEFINITION = [
    {
        "name": "procurementMethod"
    },
    {
        "name": "auctionID"
    },
    {
        "name": "minNumberOfQualifiedBids",
        "required": True
    },
    {
        "name": "enquiryPeriod"
    },
    {
        "name": "submissionMethod"
    },
    {
        "name": "awardCriteria"
    },
    {
        "name": "owner"
    },
    {
        "name": "id"
    },
    {
        "name": "tenderPeriod"
    },
    {
        "name": "documents",
        'model': [
            {
                "name": "id",
            },
            {
                "name": "documentType",
            },
            {
                "name": "title",
                "multilang": True,
                "required": True
            },
            {
                "name": "title",
                "multilang": True
            },
            {
                "name": "format",
            },
            {
                "name": "url",
            },
            {
                "name": "datePublished",
            },
            {
                "name": "dateModified",
            },
            {
                "name": "language",
            },
            {
                "name": "documentOf",
                "required": True
            },
            {
                "name": "relatedItem",
            },
            {
                "name": "index",
            },
            {
                "name": "accessDetails",
            },
        ]
    },
    {
        "name": "title",
        "required": True,
        'multilang': True
    },
    {
        "name": "tenderAttempts",
        "required": True
    },
    {
        "name": "guarantee",
        "required": True,
        'model': {}
    },
    {
        "name": "dateModified"
    },
    {
        "name": "status"
    },
    {
        "name": "description",
        "required": True,
        'multilang': True
    },
    {
        "name": "auctionPeriod",
        "required": True
    },
    {
        "name": "procurementMethodType",
        "required": True
    },
    {
        "name": "lotIdentifier",
        "required": True
    },
    {
        "name": "date"
    },
    {
        "name": "rectificationPeriod"
    },
    {
        "name": "minimalStep",
        "required": True,
        "model": {}
    },
    {
        "name": "items",
        "required": True,
        "model": [
            {
                "name": "description",
                "required": True,
                'multilang': True
            },
            {
                "name": "id"
            },
            {
                "name": "classification",
                "required": True,
                "model":
                [
                    {
                        "name": "scheme",
                        "required": True
                    },
                    {
                        "name": "id",
                        "required": True
                    },
                    {
                        "name": "description",
                        "required": True
                    },
                    {
                        "name": "uri"
                    }
                ]
            },
            {
                "name": "additionalClassifications",
                "required": True,
                "model":
                [
                    {
                        "name": "scheme",
                        "required": True
                    },
                    {
                        "name": "id",
                        "required": True
                    },
                    {
                        "name": "description",
                        "required": True
                    },
                    {
                        "name": "uri"
                    }
                ]
            },
            {
                "name": "unit",
                "required": True,
                "model":
                [
                    {
                        "name": "code",
                        "required": True
                    },
                    {
                        "name": "name"
                    },
                    {
                        "name": "quantity",
                        "required": True
                    },
                    {
                        "name": "address",
                        "required": True,
                        "model": [


                        ]
                    },
                    {
                        "name": "location"
                    },

                ]
            }
        ]
    },
    {
        "name": "value",
        "required": True,
        "model": {}
    },
    {
        "name": "procuringEntity",
        "required": True,
        "model": [
            {
                "name": "name",
                "required": True,
                "multilang": True
            },
            {
                "name": "identifier",
                "required": True,
                "model": [
                    {
                        "name": "scheme",
                        "required": True
                    },
                    {
                        "name": "id",
                        "required": True
                    },
                    {
                        "name": "legalName",
                        "multilang": True
                    },
                    {
                        "name": "uri"
                    }
                ],
            },
            {
                "name": "additionalIdentifiers",
                "required": True,
                "model": [
                    {
                        "name": "scheme",
                        "required": True
                    },
                    {
                        "name": "id",
                        "required": True
                    },
                    {
                        "name": "legalName",
                        "multilang": True
                    },
                    {
                        "name": "uri"
                    }
                ],
            },
            {
                "name": "address",
                "required": True,
                "model": [
                    {
                        "name": "streetAddress",
                    },
                    {
                        "name": "locality",
                    },
                    {
                        "name": "region",
                    },
                    {
                        "name": "postalCode",
                    },
                    {
                        "name": "id"
                    },
                    {
                        "name": "countryName",
                        "required": True,
                        "multilang": True
                    },
                    {
                        "name": "uri"
                    }
                ],
            },
            {
                "name": "contactPoint",
                "required": True,
                "model": [
                    {
                        "name": "name",
                        "required": True,
                        "multilang": True
                    },
                    {
                        "name": "email",
                    },
                    {
                        "name": "telephone",
                    },
                    {
                        "name": "faxNumber",
                    },
                    {
                        "name": "url",
                    },
                    {
                        "name": "id"
                    }
                ],
            },
            {
                "name": "kind"
            }
        ]
    },
    {
        "name": "lotHolder",
        "required": True,
        "model": [
            {
                "name": "name",
                "required": True,
                "multilang": True
            },
            {
                "name": "identifier",
                "required": True,
                "model": [
                    {
                        "name": "scheme",
                        "required": True
                    },
                    {
                        "name": "id",
                        "required": True
                    },
                    {
                        "name": "legalName",
                        "multilang": True
                    },
                    {
                        "name": "uri"
                    }
                ],
            },
            {
                "name": "additionalIdentifiers",
                "required": True,
                "model": [
                    {
                        "name": "scheme",
                        "required": True
                    },
                    {
                        "name": "id",
                        "required": True
                    },
                    {
                        "name": "legalName",
                        "multilang": True
                    },
                    {
                        "name": "uri"
                    }
                ],
            },
            {
                "name": "address",
                "model": [
                    {
                        "name": "streetAddress",
                    },
                    {
                        "name": "locality",
                    },
                    {
                        "name": "region",
                    },
                    {
                        "name": "postalCode",
                    },
                    {
                        "name": "id"
                    },
                    {
                        "name": "countryName",
                        "required": True,
                        "multilang": True
                    },
                    {
                        "name": "uri"
                    }
                ],
            },
            {
                "name": "contactPoint",
                "model": [
                    {
                        "name": "name",
                        "required": True,
                        "multilang": True
                    },
                    {
                        "name": "email",
                    },
                    {
                        "name": "telephone",
                    },
                    {
                        "name": "faxNumber",
                    },
                    {
                        "name": "url",
                    },
                    {
                        "name": "id"
                    }
                ],
            },
            {
                "name": "kind"
            }
        ]
    },
    {
        "name": "registrationFee",
        "required": True,
        "model": [
            {
                "name": "amount",
                "required": True
            },
            {
                "name": "currency",
                "required": True
            }
        ]
    },
    {
        "name": "bankAccount",
        "model":
        [
            {
                "name": "description",
                "multilang": True
            },
            {
                "name": "bankName",
                "required": True
            },
            {
                "name": "accountIdentification",
                "required": True,
                "model":
                [
                    {
                        "name": "scheme",
                        "required": True
                    }
                ]
            },
        ]
    },
    {
        "name": "contractTerms",
        "required": True,
        "model": [
            {
                "name": "type"
            },
            {
                "name": "leaseTerms",
                "required": True,
                "model": [
                    {
                        "name": "leaseDuration",
                        "required": True
                    }
                ]
            }
        ]
    },
    {"name": "mode"},
    {"name": "procurementMethodDetails"},
    {"name": "submissionMethodDetails"},
    {"name": "auctionParameters", "model": [{"name": "type"}]},
    {"name": "budgetSpent", "required": True, "model": []},
]
