### dataset_processing.py

import pandas as pd
from scipy.io import arff

def preprocess_kaggle_data(file_path):
    kaggle_data = pd.read_csv(file_path)
    kaggle_data['url_length'] = kaggle_data['url'].apply(len)
    kaggle_data['has_at_symbol'] = kaggle_data['url'].apply(lambda x: 1 if '@' in x else 0)
    kaggle_data['is_https'] = kaggle_data['url'].apply(lambda x: 1 if x.lower().startswith('https://') else 0)
    kaggle_data['num_dots'] = kaggle_data['url'].apply(lambda x: x.count('.'))
    kaggle_data['contains_suspicious_words'] = kaggle_data['url'].apply(lambda x: 1 if any(word in x.lower() for word in ["login", "secure", "verify", "bank", "account"]) else 0)

    # Ensure the 'type' column has consistent labels
    kaggle_data['phishing'] = kaggle_data['type'].apply(lambda x: 1 if x.lower() == 'phishing' else 0)
    return kaggle_data

def load_arff_data(file_path):
    data, meta = arff.loadarff(file_path)
    df = pd.DataFrame(data)
    
    # Print the columns for debugging
    print("Columns in the DataFrame:", df.columns)
    
    # Adjust the column names according to the actual columns in the ARFF file
    df['url_length'] = df['URL'].apply(len)
    df['has_at_symbol'] = df['URL'].apply(lambda x: 1 if '@' in x else 0)
    df['is_https'] = df['URL'].apply(lambda x: 1 if x.lower().startswith('https://') else 0)
    df['num_dots'] = df['URL'].apply(lambda x: x.count('.'))
    df['contains_suspicious_words'] = df['URL'].apply(lambda x: 1 if any(word in x.lower() for word in ["login", "secure", "verify", "bank", "account"]) else 0)
    df['phishing'] = df['Result'].apply(lambda x: 1 if x == b'phishing' else 0)
    
    return df