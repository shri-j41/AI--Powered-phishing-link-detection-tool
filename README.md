# ai-powered-phishing-link-detection
# Phishing Detection Tool
# since the csv file is tool big , which i was unable to upload here in my repo . pull a request so that i can provide you csv file via mail.

This project is an AI-powered phishing detection tool that uses a RandomForestClassifier to classify URLs as either "Phishing" or "Legitimate". The tool includes a GUI for user interaction and a database to store prediction history.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [Model Training](#model-training)
- [GUI and Database](#gui-and-database)
- [Contributing](#contributing)
- [License](#license)
- [Future Work](#future-work)
- [Acknowledgements](#acknowledgements)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/shri-j41/ai-powered-phishing-link-detection.git
    ```

2. Navigate to the project directory:
    ```sh
    cd phishing_detection_tool
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Ensure you have the dataset files in the `data` directory.
2. Run the main script to start the application:
    ```sh
    python phishing_tool_main.py
    ```

## Project Structure

```
phishing_detection_tool/
│
├── data/
│   ├── malicious_phish.csv
│   ├── Training Dataset.arff
│   └── .old.arff
│
├── phishing_tool_main.py
├── gui_and_db.py
├── dataset_processing.py
├── requirements.txt
└── README.md
```

## Dataset

The tool uses a CSV dataset from Kaggle and ARFF datasets for training. The datasets should be placed in the `data` directory.

## Model Training

The model is trained using a RandomForestClassifier. The training process includes:
- Loading and preprocessing the dataset.
- Feature selection using SelectKBest with chi-squared scoring.
- Splitting the data into training and testing sets.
- Training the RandomForest model.
- Evaluating the model's accuracy and generating a classification report.

## GUI and Database

The tool includes a GUI built with Tkinter for user interaction. Users can input URLs to classify and view prediction history. The predictions are stored in an SQLite database.

### GUI Features
- URL Classification
- Prediction History

### Database Schema
- `predictions` table:
    - `id`: INTEGER PRIMARY KEY AUTOINCREMENT
    - `url`: TEXT
    - `url_length`: INTEGER
    - `has_at_symbol`: INTEGER
    - `is_https`: INTEGER
    - `num_dots`: INTEGER
    - `contains_suspicious_words`: INTEGER
    - `prediction`: TEXT

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.


## Future Work

- Implement additional machine learning models for comparison.
- Enhance the feature extraction process.
- Develop a web-based interface for broader accessibility.
- Integrate real-time URL scanning capabilities.

## Acknowledgements

- The dataset used in this project is sourced from Kaggle.
- Special thanks to the open-source community for their valuable tools and libraries.

## Created by Shrijal ESmali.
