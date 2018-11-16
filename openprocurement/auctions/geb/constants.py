from datetime import timedelta

# --DOCUMETS contstants--------------------------------------------------------

# document type for ofline documents
DOCUMENT_TYPE_OFFLINE = ['x_dgfAssetFamiliarization']

# auction resource document types
AUCTION_DOCUMENT_TYPES = [
    'technicalSpecifications',
    'evaluationCriteria',
    'clarifications',
    'billOfQuantity',
    'conflictOfInterest',
    'evaluationReports',
    'complaints',
    'eligibilityCriteria',
    'tenderNotice',
    'illustration',
    'x_financialLicense',
    'x_virtualDataRoom',
    'x_dgfAssetFamiliarization',
    'x_presentation',
    'x_nda',
    'x_qualificationDocuments',
    'cancellationDetails',
    'contractProforma'
    ]

# bid resource document types
BID_DOCUMENT_TYPES = [
    'commercialProposal',
    'qualificationDocuments',
    'eligibilityDocuments',
]


# cancellation document type
CANCELLATION_DOCUMENT_TYPES = ['cancellationDetails']

# --AUCTION contstants---------------------------------------------------------

# which type of auction will be in module auction
AUCTION_PARAMETERS_TYPE = 'texas'

# auction resource statuses
AUCTION_STATUSES = [
    'draft',
    'active.rectification',
    'active.tendering',
    'active.enquiry',
    'active.auction',
    'active.qualification',
    'active.awarded',
    'unsuccessful',
    'cancelled',
    'complete'
]

# in this auction resource statuses can delete bids
AUCTION_STATUSES_FOR_DELETING_BIDS = [
    'active.tendering',
    'active.enquiry'
]

# in this auction resource statuses can patch auction fields
AUCTION_STATUSES_FOR_PATCHING_AUCTION = [
    'active.rectification'
]

# in this auction resource statuses can patch bids
AUCTION_STATUSES_FOR_PATCHING_BIDS = [
    'active.tendering',
    'active.enquiry'
]

# after cancellation was created
# if auction resource was in this statuses
# all bids will be deleted
AUCTION_STATUSES_FOR_CLEAN_BIDS_IN_CANCELLATION = [
    'active.tendering',
    'active.enquiry',
    'active.auction'
]

# in this auctioon resource statuses: nobody can`t get bid (only bid owner)
AUCTION_STATUSES_FOR_FORBIDDEN_GET_BIDS = [
    'active.tendering',
    'active.enquiry',
    'active.auction'
]

# in this auction resource statuses can post questions
AUCTION_STATUSES_FOR_ADDING_QUESTIONS = [
    'active.rectification',
    'active.tendering',
    'active.enquiry'
]

# in this auctioon resource statuses: can patch auction document
AUCTION_STATUSES_FOR_PATCHING_DOCUMENTS_STATUSES = [
    'active.rectification',
    'active.tendering',
    'active.enquiry'
]

# statuses in which can put auction document
AUCTION_STATUSES_FOR_PUT_DOCUMENTS_STATUSES = [
    'active.rectification',
    'active.tendering',
    'active.enquiry',
    'active.qualification',
    'active.awarded'
]


# in this auction resource statuses can post auction documents
AUCTION_STATUSES_FOR_ADDING_DOCUMENTS = [
    'active.rectification',
    'active.tendering',
    'active.enquiry'
]

# auction resoure statuses in which module auction can post document
AUCTION_STATUSES_FOR_MODULE_AUCTION_ADDING_DOCUMENTS = [
    'active.auction',
    'active.qualification'
]

# in this auction resource statuses can patch(answer) questions
AUCTION_STATUSES_FOR_CHANGING_QUESTIONS = [
    'active.rectification',
    'active.tendering',
    'active.enquiry'
]

# in this auction resource statuses can patch items
AUCTION_STATUSES_FOR_CHANGING_ITEMS = ['active.rectification']

# in this auction resource statuses can post bid document
AUCTION_STATUSES_FOR_ADDING_BID_DOCUMENTS = [
    'active.tendering',
    'active.enquiry',
    'active.qualification'
]

# duration of rectification period
AUCTION_RECTIFICATION_PERIOD_DURATION = timedelta(hours=48)


# --BID contstants-------------------------------------------------------------

# bid resource statuses
BID_STATUSES = [
    'draft',
    'pending',
    'active',
    'unsuccessful',
    'invalid'
]

# in this bid statuses: can patch bid
BID_STATUSES_FOR_PATCHING = [
    'pending',
    'active'
]

# in this bid statuses: can delete bid
BID_STATUSES_FOR_DELETING = [
    'draft',
    'pending',
    'active'
]

# in this bid statuses: can post bid document
BID_STATUSES_FOR_ADDING_BID_DOCUMENTS = [
    'draft',
    'pending',
    'active'
]

# --ITEM contstants------------------------------------------------------------

# types of item resource additional classificators
ITEM_ADDITIONAL_CLASSIFICATIONS_TYPES = (
    u'CPVS',
    u'cadastralNumber',
    u'kvtspz'
)

# --GENERAL contstants---------------------------------------------------------

# cav ps codes for Classification
CAV_PS_CODES = [
    "06110000-6",
    "06111000-3",
    "06112000-0",
    "06120000-9",
    "06121000-6",
    "06122000-3",
    "06123000-0",
    "06124000-7",
    "06125000-4",
    "06126000-1",
    "06127000-8",
    "06128000-5",
    "06129000-2"
]

# if level of accreditation not defined in the config file, then use these
DEFAULT_LEVEL_OF_ACCREDITATION = {
    'create': [1],
    'edit': [2]
}

# if 'use_default' defined in the config file, then use these
DEFAULT_PROCUREMENT_METHOD_TYPE = "landlease"
