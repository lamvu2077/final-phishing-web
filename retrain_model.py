#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to retrain model with new scikit-learn version
"""

import sys
import io
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
import warnings
warnings.filterwarnings('ignore')

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Loading data...")
# Load data
data = pd.read_csv("phishing.csv")
print(f"Loaded {len(data)} rows")

# Split features and target
X = data.drop(["class"], axis=1)
y = data["class"]

# Remove Index column if exists (not needed for training)
if "Index" in X.columns:
    X = X.drop(["Index"], axis=1)

print(f"Number of features: {X.shape[1]}")
print(f"Class distribution:\n{y.value_counts()}")

# Split data: 80-20
print("\nSplitting data into train/test (80-20)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Train set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# Train model with Logistic Regression
print("\nTraining Logistic Regression...")
print("(This may take a few minutes...)")

gbc = LogisticRegression(max_iter=1000, random_state=42, solver='lbfgs')
gbc.fit(X_train, y_train)

# Evaluate model
print("\nEvaluating model...")
train_score = gbc.score(X_train, y_train)
test_score = gbc.score(X_test, y_test)

print(f"Accuracy on train set: {train_score:.4f}")
print(f"Accuracy on test set: {test_score:.4f}")

# Save model
print("\nSaving model to pickle/model.pkl...")
with open('pickle/model.pkl', 'wb') as file:
    pickle.dump(gbc, file)

print("\nDone! Model trained and saved successfully.")
print("Now you can run: python app.py")

