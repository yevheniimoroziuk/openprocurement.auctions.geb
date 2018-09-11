
from schematics.transforms import whitelist

auction_create_role = whitelist(
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


auction_contractTerms_create_role = whitelist('leaseTerms')

auction_active_rectification_role = whitelist(
    'auctionID',
    'auctionParameters',
    'auctionPeriod',
    'awardCriteria',
    'bankAccount',
    'budgetSpent',
    'contractTerms',
    'date',
    'dateModified',
    'description',
    'description_en',
    'description_ru',
    'enquiryPeriod',
    'guarantee',
    'doc_id',
    'items',
    'lotHolder',
    'lotIdentifier',
    'minNumberOfQualifiedBids',
    'minimalStep',
    'owner',
    'procurementMethod',
    'procurementMethodType',
    'procuringEntity',
    'rectificationPeriod',
    'registrationFee',
    'status',
    'submissionMethod',
    'tenderAttempts',
    'tenderPeriod',
    'title',
    'title_en',
    'title_ru',
    'value'
)

auction_edit_rectification_role = whitelist(
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
    'minimalStep',
    'procuringEntity',
    'registrationFee',
    'tenderAttempts',
    'title',
    'title_en',
    'title_ru',
    'value'
)

bid_view_role = whitelist(
    'id',
    'status',
    'tenderers',
    'value',
)

bid_pending_role = whitelist(
    'id',
    'status',
    'tenderers',
    'value',
    'date',
    'id',
    'owner',
    'qualified',
)

bid_edit_pending_role = whitelist(
    'id',
    'status',
    'tenderers',
    'value',
    'date',
    'id',
    'owner',
    'qualified',
)

bid_active_role = whitelist(
    'id',
    'status',
    'tenderers',
    'value',
    'date',
    'id',
    'owner',
    'qualified',
    'bidNumber'
)

bid_edit_active_role = whitelist(
    'id',
    'status',
    'tenderers',
    'value',
    'date',
    'id',
    'owner',
    'qualified',
    'bidNumber'
)

bid_create_role = whitelist(
    'value',
    'status',
    'tenderers'
)


bid_edit_draft_role = whitelist(
    'value',
    'status',
    'tenderers'
)
