import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_selection import SelectKBest, chi2
from dataset_processing import preprocess_kaggle_data, load_arff_data
from gui_and_db import setup_database, create_gui

# Step 1: Load and Preprocess Dataset
file_path = r'C:\Users\N I T R O 5\OneDrive - Coventry University\Desktop\3rd sem\programming and algirthm 2\course work\Phishing_Detection_tool\data\malicious_phish.csv'
training_arff_path = r'C:\Users\N I T R O 5\OneDrive - Coventry University\Desktop\3rd sem\programming and algirthm 2\course work\Phishing_Detection_tool\Training Dataset.arff'
old_arff_path = r'C:\Users\N I T R O 5\OneDrive - Coventry University\Desktop\3rd sem\programming and algirthm 2\course work\Phishing_Detection_tool\.old.arff'

if os.path.exists(file_path):
    kaggle_data = preprocess_kaggle_data(file_path)
elif os.path.exists(training_arff_path):
    kaggle_data = load_arff_data(training_arff_path)
elif os.path.exists(old_arff_path):
    kaggle_data = load_arff_data(old_arff_path)
else:
    raise FileNotFoundError("No dataset found. Please provide a valid dataset.")

# Feature Selection
X_kaggle = kaggle_data[['url_length', 'has_at_symbol', 'is_https', 'num_dots', 'contains_suspicious_words']]
y_kaggle = kaggle_data['phishing']

feature_selector = SelectKBest(score_func=chi2, k='all')
X_kaggle_selected = feature_selector.fit_transform(X_kaggle, y_kaggle)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_kaggle_selected, y_kaggle, test_size=0.3, random_state=42)

# Step 2: Train the Model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate the Model
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("Classification Report:\n", classification_report(y_test, y_pred))

# Step 3: Set Up Database and Populate with CSV Data
conn, c = setup_database()

for _, row in kaggle_data.iterrows():
    c.execute('''INSERT INTO predictions (url, url_length, has_at_symbol, is_https, num_dots, contains_suspicious_words, prediction)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', 
              (row['url'], row['url_length'], row['has_at_symbol'], row['is_https'], row['num_dots'], row['contains_suspicious_words'], 'Phishing' if row['phishing'] == 1 else 'Legitimate'))
conn.commit()

# The GUI is created using the `create_gui` function, which takes the trained model, feature selector, and database connection as inputs.
create_gui(rf_model, feature_selector, conn, c, kaggle_data, kaggle_data)

# Close the database connection when the application ends
conn.close()
