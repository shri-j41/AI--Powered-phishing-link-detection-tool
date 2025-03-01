### gui_and_db.py

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_database():
    conn = sqlite3.connect('phishing_detection.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            url_length INTEGER,
            has_at_symbol INTEGER,
            is_https INTEGER,
            num_dots INTEGER,
            contains_suspicious_words INTEGER,
            prediction TEXT
        )
    ''')
    conn.commit()
    return conn, c

def create_gui(rf_model, feature_selector, conn, c, training_data, old_data):
    def classify_url():
        try:
            input_url = url_entry.get().strip()

            # Check for well-known legitimate URLs
            well_known_legitimate_urls = ["https://www.youtube.com", "https://www.google.com", "https://www.facebook.com"]
            if any(input_url.startswith(url) for url in well_known_legitimate_urls):
                result = "Legitimate"
            else:
                # Check in training ARFF data
                training_result = training_data.get(input_url)
                if training_result:
                    result = training_result
                else:
                    # Check in old ARFF data
                    old_result = old_data.get(input_url)
                    if old_result:
                        result = old_result
                    else:
                        # Look up the classification result from the database
                        c.execute('SELECT prediction FROM predictions WHERE url = ?', (input_url, ))
                        result = c.fetchone()

                        if result:
                            result = result[0]
                        else:
                            # Extract URL features
                            url_length = len(input_url)
                            has_at_symbol = 1 if '@' in input_url else 0
                            is_https = 1 if input_url.lower().startswith('https://') else 0
                            num_dots = input_url.count('.')
                            contains_suspicious_words = 1 if any(word in input_url.lower() for word in ["login", "secure", "verify", "bank", "account"]) else 0

                            user_data = pd.DataFrame({
                                "url_length": [url_length],
                                "has_at_symbol": [has_at_symbol],
                                "is_https": [is_https],
                                "num_dots": [num_dots],
                                "contains_suspicious_words": [contains_suspicious_words],
                            })

                            # Feature Selection
                            user_data_selected = feature_selector.transform(user_data)
                            prediction = rf_model.predict(user_data_selected)
                            result = "Phishing" if prediction[0] == 1 else "Legitimate"

                            # Save prediction to the database
                            c.execute('''INSERT INTO predictions (url, url_length, has_at_symbol, is_https, num_dots, contains_suspicious_words, prediction)
                                         VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                                      (input_url, url_length, has_at_symbol, is_https, num_dots, contains_suspicious_words, result))
                            conn.commit()

            messagebox.showinfo("Result", f"The URL is classified as: {result}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def view_predictions():
        try:
            logging.info("Fetching prediction history from the database...")
            top = tk.Toplevel(root)
            top.title("Prediction History")

            history_label = tk.Label(top, text="Prediction History:")
            history_label.pack()

            frame = tk.Frame(top)
            frame.pack(fill=tk.BOTH, expand=True)

            tree = ttk.Treeview(frame, columns=("ID", "URL", "Length", "Contains @", "HTTPS", "Dots", "Suspicious Words", "Prediction"), show='headings')
            tree.heading("ID", text="ID")
            tree.heading("URL", text="URL")
            tree.heading("Length", text="Length")
            tree.heading("Contains @", text="Contains @")
            tree.heading("HTTPS", text="HTTPS")
            tree.heading("Dots", text="Dots")
            tree.heading("Suspicious Words", text="Suspicious Words")
            tree.heading("Prediction", text="Prediction")

            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree.pack(fill=tk.BOTH, expand=True)

            c.execute('SELECT * FROM predictions')
            rows = c.fetchall()

            for row in rows:
                tree.insert("", "end", values=row)

            logging.info("Prediction history successfully displayed.")
        except Exception as e:
            logging.error(f"An error occurred while fetching prediction history: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def blink():
        current_color = url_label.cget("foreground")
        next_color = "black" if current_color == "green" else "green"
        url_label.config(foreground=next_color)
        root.after(500, blink)

    def matrix_effect():
        footer_label.config(text="Made by Shri-j41")
        footer_label.after(100, lambda: footer_label.config(text=""))

    root = tk.Tk()
    root.title("AI-powered Phishing Detection Tool")
    root.geometry("800x600")  # Set the size of the GUI

    # Set color theme to a more visually appealing combination
    root.configure(bg='white')
    style = ttk.Style()
    style.configure("TLabel", background='white', foreground='blue', font=("Arial", 12))
    style.configure("TButton", background='white', foreground='blue', font=("Arial", 12))
    style.configure("TEntry", fieldbackground='white', foreground='blue', font=("Arial", 12))
    style.configure("Treeview", background='white', foreground='black', fieldbackground='white', font=("Arial", 12))
    style.configure("Treeview.Heading", background='white', foreground='blue', font=("Arial", 12))

    url_label = ttk.Label(root, text="Enter URL:")
    url_label.pack(pady=10)
    blink()  # Start blinking effect

    url_entry = ttk.Entry(root, width=50)
    url_entry.pack(pady=10)

    classify_button = ttk.Button(root, text="Classify URL", command=classify_url)
    classify_button.pack(pady=10)

    history_button = ttk.Button(root, text="View Prediction History", command=view_predictions)
    history_button.pack(pady=10)

    footer_label = ttk.Label(root, text="", font=("Arial", 10))
    footer_label.pack(side=tk.BOTTOM, pady=10)
    matrix_effect()  # Start matrix effect

    created_by_label = ttk.Label(root, text="Created by Shrijal Esmali", font=("Arial", 10))
    created_by_label.pack(side=tk.BOTTOM, pady=5)

    root.mainloop()