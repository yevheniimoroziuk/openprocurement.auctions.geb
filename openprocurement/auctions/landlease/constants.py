from datetime import timedelta

API_DOCUMENT_STATUSES = ['active.rectification', 'active.tendering']
AUCTION_DOCUMENT_STATUSES = ['active.auction', 'active.qualification']

# duration of periods
RECTIFICATION_PERIOD_DURATION = timedelta(days=2)
TENDER_PERIOD_DURATION = timedelta(days=3)                                      # TODO if need 20:00 time


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
        'cancellationDetails'
    ]
BID_DOCUMENT_TYPES = [
   'commercialProposal',
   'qualificationDocuments',
   'eligibilityDocuments',
]
NUMBER_OF_BIDS_TO_BE_QUALIFIED = 2
DEFAULT_LEVEL_OF_ACCREDITATION = {'create': [1],                                # TODO ask what permissions
                                  'edit': [2]}

DEFAULT_PROCUREMENT_METHOD_TYPE = "landlease"
AUCTION_PARAMETERS_TYPE = 'texas'

AUCTION_STATUSES = ['draft',
                    'active.rectification',
                    'active.tendering',
                    'active.enquiry',
                    'active.auction',
                    'active.qualification',
                    'active.awarded',
                    'unsuccessful',
                    'cancelled',
                    'complete']

BID_STATUSES = ['draft', 'pending', 'active', 'deleted']
