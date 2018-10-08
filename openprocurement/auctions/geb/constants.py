from datetime import timedelta

PROCEDURE_DOCUMENT_STATUSES = ['active.rectification', 'active.tendering', 'active.enquiry']
AUCTION_DOCUMENT_STATUSES = ['active.auction', 'active.qualification']

# duration of periods
RECTIFICATION_PERIOD_DURATION = timedelta(days=2)
MIN_NUMBER_OF_DAYS_TENDERING = timedelta(days=1)


# documets
DOCUMENT_TYPE_OFFLINE = ['x_dgfAssetFamiliarization']
DOCUMENT_TYPE_URL_ONLY = ['virtualDataRoom']

AUCTION_DOCUMENT_TYPES = [
        'technicalSpecifications',
        'evaluationCriteria',
        'clarifications',
        'billOfQuantity',
        'conflictOfInterest',
        'evaluationReports',
        'eligibilityCriteria',
        'tenderNotice',
        'illustration',
        'x_financialLicense',
        'x_virtualDataRoom',
        'x_dgfAssetFamiliarization',
        'x_presentation',
        'x_nda',
        'x_qualificationDocuments',
        'cancellationDetails'
    ]

BID_DOCUMENT_TYPES = [
    'commercialProposal',
    'qualificationDocuments',
    'eligibilityDocuments',
]
NUMBER_OF_BIDS_TO_BE_QUALIFIED = 2

DEFAULT_LEVEL_OF_ACCREDITATION = {
    'create': [1],                                # TODO ask what permissions
    'edit': [2]
}

DEFAULT_PROCUREMENT_METHOD_TYPE = "landlease"
AUCTION_PARAMETERS_TYPE = 'texas'

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

AUCTION_STATUS_FOR_DELETING_BIDS = [
    'active.tendering',
    'active.enquiry'
]

AUCTION_STATUS_FOR_ADDING_QUESTIONS = [
    'active.tendering',
    'active.enquiry'
]

AUCTION_STATUS_FOR_CHANGING_QUESTIONS = [
    'active.tendering',
    'active.enquiry'
]

BID_STATUSES = [
    'draft',
    'pending',
    'active',
    'unsuccessful'
]

BID_STATUSES_FOR_ADDING_DOCUMENTS = [
    'active.tendering',
    'active.enquiry',
    'active.qualification'
]


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

GEB_ITEM_ADDITIONAL_CLASSIFICATIONS = (
    u'CPVS',
    u'cadastralNumber',
    u'kvtspz'
)
MIN_NUMBER_OF_DAY_BEFORE_AUCTION = 6
