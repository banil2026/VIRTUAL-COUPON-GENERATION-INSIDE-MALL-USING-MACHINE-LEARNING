import pandas as pd

def preprocess_dataset(csv_file_path):
    df = pd.read_csv(csv_file_path)
    df.drop_duplicates(inplace=True)
    
    # Example transformation (normalize numeric features)
    if 'amount_spent' in df.columns:
        df['amount_spent'] = df['amount_spent'] / df['amount_spent'].max()
    if 'visits' in df.columns:
        df['visits'] = df['visits'] / df['visits'].max()
    
    # Optional: Encode categorical variables if added in future
    return df

