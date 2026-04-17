import pandas as pd

KEYWORD_RULES = {
    "rent": ["WT FED"],
    "reimbursement": ["ZELLE FROM JASON TRUONG NGUYEN", "ZELLE FROM LY BRANDON", 
                      "ZELLE FROM TRAN BRANDON", "ZELLE FROM NGUYEN KADEN",
                      "ONLINE TRANSFER FROM VO D EVERYDAY"],
    "utilities": ["ZELLE TO CURTIS", "SO CAL EDISON"],
    "shopping": ["MICHAELS STORES", "LAZ PARKING"],
    "subscriptions": ["SPOTIFY", "APPLE.COM/BILL", "OPENAI.COM", "ABC*40120", "PLAYSTATION"],
    "dining": ["IN-N-OUT", "CAVA", "DLR", "TACOS"],
    "personal_care": ["AESOP"],
    "groceries": ["TRADER JOE", "RALPHS"],
    "savings": ["GOLDMAN SACHS", "ROBINHOOD"],
    "credit_card": ["CHASE CREDIT CRD", "DISCOVER"],
    "income": ["UNIVERSITY OF CA", "VENMO CASHOUT"]
}

def classify_transaction(description: str) -> str:
    """
    Based on a given transaction's description, returns the correct category of
    the transaction.
    
    Ex: "SO CAL EDISON CO BILL PAYMT" -> utilities

    Args:
        description (str): Transaction description

    Returns:
        str: Category of transaction.
    """
    upper_desc = description.upper()

    for categ, desc in KEYWORD_RULES.items():
        for item in desc:
            if item in upper_desc:
                return categ
    return "uncategorized"

def classify_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Iterates through transactions dataframe, updating each transaction's category column into
    their respective category from classify_transaction.

    Args:
        df (pd.DataFrame): Transactions DataFrame

    Returns:
        pd.DataFrame: Updated DataFrame with categories filled out
    """
    for index,row in df.iterrows():
        if pd.isna(row['category']) or row['category'] == 'uncategorized':
            df.at[index, 'category'] = classify_transaction(row['description'])
            
    return df
