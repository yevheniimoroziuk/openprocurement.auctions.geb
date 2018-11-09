
from schematics.transforms import whitelist

auction_draft_role = whitelist(
    'auctionID',
    'auctionParameters',
    'auctionPeriod',
    'awardCriteria'
    'budgetSpent',
    'cancellations',
    'contractTerms',
    'date',
    'dateModified',
    'description',
    'doc_id',
    'guarantee',
    'items',
    'lotHolder',
    'lotIdentifier',
    'minNumberOfQualifiedBids',
    'minimalStep',
    'mode',
    'owner',
    'procurementMethod',
    'procurementMethodDetails',
    'procurementMethodType',
    'procuringEntity',
    'registrationFee',
    'status',
    'submissionMethod',
    'submissionMethodDetails',
    'tenderAttempts',
    'title',
    'value'
)

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


auction_contractTerms_create_role = whitelist('leaseTerms', 'type')

auction_rectification_role = whitelist(
    'auctionID',
    'auctionParameters',
    'auctionPeriod',
    'awardCriteria',
    'bankAccount',
    'budgetSpent',
    'contractTerms',
    'date',
    'cancellations',
    'dateModified',
    'description',
    'description_en',
    'description_ru',
    'doc_id',
    'documents',
    'enquiryPeriod',
    'guarantee',
    'items',
    'mode',
    'procurementMethodDetails',
    'submissionMethodDetails',
    'lotHolder',
    'lotIdentifier',
    'minNumberOfQualifiedBids',
    'minimalStep',
    'owner',
    'procurementMethod',
    'procurementMethodType',
    'procuringEntity',
    'questions',
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

auction_tendering_role = whitelist(
    'auctionID',
    'auctionParameters',
    'auctionPeriod',
    'awardCriteria',
    'bankAccount',
    'cancellations',
    'budgetSpent',
    'contractTerms',
    'date',
    'dateModified',
    'description',
    'description_en',
    'description_ru',
    'doc_id',
    'mode',
    'procurementMethodDetails',
    'submissionMethodDetails',
    'documents',
    'enquiryPeriod',
    'guarantee',
    'items',
    'lotHolder',
    'lotIdentifier',
    'minNumberOfQualifiedBids',
    'minimalStep',
    'owner',
    'procurementMethod',
    'procurementMethodType',
    'procuringEntity',
    'questions',
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

auction_enquiry_role = whitelist(
    'auctionID',
    'auctionParameters',
    'auctionPeriod',
    'awardCriteria',
    'bankAccount',
    'budgetSpent',
    'cancellations',
    'contractTerms',
    'date',
    'dateModified',
    'description',
    'description_en',
    'description_ru',
    'doc_id',
    'procurementMethodDetails',
    'mode',
    'submissionMethodDetails',
    'documents',
    'enquiryPeriod',
    'guarantee',
    'items',
    'lotHolder',
    'lotIdentifier',
    'minNumberOfQualifiedBids',
    'minimalStep',
    'owner',
    'procurementMethod',
    'procurementMethodType',
    'procuringEntity',
    'questions',
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

auction_edit_enquiry_role = whitelist()

auction_edit_tendering_role = whitelist()

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

question_enquiry_role = whitelist(
    'date',
    'title',
    'description',
    'questionOf',
    'relatedItem',
    'id'
)
question_rectification_role = question_enquiry_role

# bid roles

bid_view_role = whitelist(
    'id',
    'status',
    'tenderers',
    'value',
    'date',
    'id',
    'owner',
    'qualified',
    'bidNumber',
    'documents',
    'participationUrl'

)

bid_pending_role = bid_view_role

bid_active_role = bid_view_role

bid_edit_pending_role = whitelist(
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


bid_active_awarded_role = bid_view_role
bid_active_qualification_role = bid_view_role
bid_active_auction_role = whitelist()
bid_active_enquiry_role = whitelist()
bid_active_tendering_role = whitelist()
bid_edit_draft_role = whitelist('status')


item_edit_role = whitelist(
        'additionalClassifications',
        'address',
        'classification',
        'description',
        'description_en',
        'description_ru',
        'quantity',
        'unit'
)

item_view_role = whitelist(
        'additionalClassifications',
        'address',
        'classification',
        'description',
        'description_en',
        'description_ru',
        'id',
        'quantity',
        'unit'
)
chronograph_view_role = whitelist(
    'auctionPeriod',
    'awardPeriod',
    'awards',
    'complaints',
    'doc_id',
    'enquiryPeriod',
    'mode',
    'numberOfBids',
    'procurementMethodType',
    'status',
    'submissionMethodDetails',
    'tenderPeriod',
    'rectificationPeriod'
)
