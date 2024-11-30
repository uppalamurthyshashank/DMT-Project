import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
data = pd.read_csv('dataset.csv')

# Select features and target
X = data[['BMI', 'Stress Level']]  # Features
y = data['Heart Attack Risk']       # Target

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Random Forest Model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf) * 100
report_rf = classification_report(y_test, y_pred_rf)

print("Random Forest Model Results:")
print(f"Accuracy: {accuracy_rf:.2f}%")
print("Classification Report:")
print(report_rf)

# Naive Bayes Model
nb_model = GaussianNB()
nb_model.fit(X_train, y_train)
y_pred_nb = nb_model.predict(X_test)
accuracy_nb = accuracy_score(y_test, y_pred_nb) * 100
report_nb = classification_report(y_test, y_pred_nb)

print("\nNaive Bayes Model Results:")
print(f"Accuracy: {accuracy_nb:.2f}%")
print("Classification Report:")
print(report_nb)
