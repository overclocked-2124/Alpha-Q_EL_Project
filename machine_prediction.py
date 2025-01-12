# Step 1: Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Step 2: Load the data
# Replace 'data.csv' with the path to your CSV file
try:
    df = pd.read_csv('efficiency_data_with_irradiance.csv')
    print("Data loaded successfully!")
    print("First few rows of the data:\n", df.head())
except FileNotFoundError:
    print("Error: File 'efficiency_data_with_irradiance.csv' not found. Please check the file path.")
    exit()

# Step 3: Create the target variable
# Define a threshold for when to rotate the panel (1) or keep it facing the sun (0)
threshold = 15.7  # Adjust this based on your project requirements
df['Decision'] = (df['Net_Efficiency'] < threshold).astype(int)
print("\nTarget variable 'Decision' created:")
print(df[['Net_Efficiency', 'Decision']].head())

# Step 4: Prepare features and target
features = ['Temperature_C', 'Irradiance_W_m2', 'Solar_Efficiency', 'TEG_Efficiency']
X = df[features]  # Features
y = df['Decision']  # Target variable
print("\nFeatures (X):\n", X.head())
print("\nTarget (y):\n", y.head())

# Step 5: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("\nData split into training and testing sets:")
print(f"Training set size: {X_train.shape[0]} samples")
print(f"Testing set size: {X_test.shape[0]} samples")

# Step 6: Train the Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)  # You can tune hyperparameters
clf.fit(X_train, y_train)
print("\nRandom Forest Classifier trained successfully!")

# Step 7: Make predictions on the test set
y_pred = clf.predict(X_test)
print("\nPredictions made on the test set.")

# Step 8: Evaluate the model
print("\nModel Evaluation:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Step 9: Use the model to make decisions for new data points
# Example: Predict whether to rotate the panel for a new set of conditions
new_data = pd.DataFrame({
    'Temperature_C': [20.5],  # Example temperature
    'Irradiance_W_m2': [1200],  # Example irradiance
    'Solar_Efficiency': [19.865],  # Example solar efficiency
    'TEG_Efficiency': [6.0653]  # Example TEG efficiency
})

# Predict the decision (0 or 1)
decision = clf.predict(new_data)
print("\nDecision for new data:", decision[0])  # Output: 0 (keep facing sun) or 1 (rotate)