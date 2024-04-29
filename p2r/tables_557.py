# id 557

# EP
enriched_proposals = {
    "organization_id": 4,
    "hard_violations_count": 1, # What about this one?
}

# EPO
enriched_proposals_orders = [
    {
        "enriched_proposals_id": 557,
        "transaction_type": "BUY",
        "quantity": 50,
        "price_value": 244.05,
        "target_quantity": 150,
    },
    {
        "enriched_proposals_id": 557,
        "transaction_type": "BUY",
        "quantity": 370,
        "price_value": 84.62,
        "target_quantity": 650,
    }
]

# EPEC
enriched_proposals_evaluated_constraints = [
    {
        "enriched_proposal_id": 557, # Note that it's singular "proposal", different from EPO
        "name": "32% < Equity < 50%",
        "violated": 1,
    }
]
