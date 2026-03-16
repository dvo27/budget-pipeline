from pathlib import Path

PROJECT_ROOT = Path(__file__).parent


# Raw Data Paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"

RAW_CHASE = RAW_DIR / "chase"
RAW_DISCOVER = RAW_DIR / "discover"
RAW_WELLS_FARGO = RAW_DIR / "wells_fargo"

# Database
DB_PATH = PROJECT_ROOT / "budget.duckdb"

BUDGET_PRESETS = {
    "50/30/20": {"needs": 0.50, "wants": 0.30, "savings": 0.20},
    "70/20/10": {"needs": 0.70, "wants": 0.20, "savings": 0.10},
    "60/30/10": {"needs": 0.60, "wants": 0.30, "savings": 0.10},
}

ACTIVE_BUDGET = "50/30/20"
BUDGET_SPLIT = BUDGET_PRESETS[ACTIVE_BUDGET]

PAY_SCHEDULE = 'biweekly'

BANK_SOURCES = {
    "wells_fargo": {
        "name": "Wells Fargo",
        "account_type": "checking",
        "raw_path": RAW_WELLS_FARGO,
        "watch_prefix": "wf_",
    },
    "chase": {
        "name": "Chase",
        "account_type": "credit_card",
        "raw_path": RAW_CHASE,
        "watch_prefix": "chase_",
    },
    "discover": {
        "name": "Discover",
        "account_type": "credit_card",
        "raw_path": RAW_DISCOVER,
        "watch_prefix": "discover_",
    },
}

CATEGORY_BUCKETS = {
    # Needs (ex. 50%)
    "rent": "needs",
    "groceries": "needs",
    "utilities": "needs",
    "gas": "needs",
    "insurance": "needs",
    "phone": "needs",
    "internet": "needs",
    "healthcare": "needs",
    "transportation": "needs",

    # Wants (ex. 30%)
    "dining": "wants",
    "entertainment": "wants",
    "subscriptions": "wants",
    "shopping": "wants",
    "travel": "wants",
    "clothing": "wants",
    "personal_care": "wants",
    "hobbies": "wants",
    "gifts": "wants",

    # Savings (ex. 20%)
    "savings": "savings",
    "investments": "savings",
    "extra_debt_payment": "savings",
    "emergency_fund": "savings",
}

TRANSACTION_SCHEMA = [
    "transaction_date",       # date — when the transaction occurred
    "post_date",              # date (nullable) — when it posted to the account
    "description",            # str — cleaned/uppercased description
    "amount",                 # float — negative = expense, positive = income
    "category",               # str (nullable) — assigned later by categorizer
    "source_bank",            # str — "wells_fargo", "chase", or "discover"
    "account_type",           # str — "checking" or "credit_card"
    "original_description",   # str — raw description before cleaning
    "transaction_id",         # str — hash for deduplication
]