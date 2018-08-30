
from schematics.transforms import whitelist

auction_create_role = (whitelist(
    'auctionPeriod',
    'bankAccount',
    'budgetSpent',
    'contractTerms',
    'description',
    'description_en',
    'description_ru',
    'guarantee',
    'items',
    'lotHolder',
    'lotIdentifier',
    'minNumberOfQualifiedBids',
    'minimalStep',
    'mode',
    'procurementMethodDetails',
    'procurementMethodType',
    'procuringEntity',
    'registrationFee',
    'submissionMethodDetails',
    'tenderAttempts',
    'title',
    'title_en',
    'title_ru',
    'value',
)
)

auction_contractTerms_create_role = (whitelist('leaseTerms'))
