import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the dataset
data = pd.read_csv('dataset.csv')

# Process Blood Pressure into separate Systolic and Diastolic columns
data[['Systolic BP', 'Diastolic BP']] = data['Blood Pressure'].str.split('/', expand=True).astype(float)

# Select features for clustering
features = data[['Cholesterol', 'Triglycerides', 'Systolic BP', 'Diastolic BP']]

# Standardize the features for better clustering performance
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Apply K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)  # Adjust n_clusters based on desired number of clusters
data['Cluster'] = kmeans.fit_predict(scaled_features)

# Output the cluster assignments along with all features
output_columns = ['Patient ID', 'Cholesterol', 'Triglycerides', 'Systolic BP', 'Diastolic BP', 'Cluster']
print("Cluster assignments for each patient with features:")
print(data[output_columns])
