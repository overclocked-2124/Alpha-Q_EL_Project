# Step 1: Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Step 2: Load the data
# Replace 'efficiency_data_with_irradiance.csv' with the path to your CSV file
try:
    df = pd.read_csv('efficiency_data_with_irradiance.csv')
    print("Data loaded successfully!")
    print("First few rows of the data:\n", df.head())
except FileNotFoundError:
    print("Error: File 'efficiency_data_with_irradiance.csv' not found. Please check the file path.")
    exit()

# Step 3: Define thresholds for classification
temp_high = 25.0  # Temperature above which the panel must cool down
temp_moderate = 20.0  # Temperature above which we consider staying up temporarily
irradiance_high = 1000  # Irradiance above which it's worth staying up temporarily

# Step 4: Create the target variable based on the three cases
def classify_decision(row, temp_high, temp_moderate, irradiance_high):
    if row['Temperature_C'] > temp_high:
        return 2  # Must cool down
    elif row['Temperature_C'] > temp_moderate and row['Irradiance_W_m2'] > irradiance_high:
        return 1  # Stay up temporarily
    else:
        return 0  # Stay up

df['Decision'] = df.apply(classify_decision, axis=1)
print("\nTarget variable 'Decision' created:")
print(df[['Temperature_C', 'Irradiance_W_m2', 'Decision']].head())

# Step 5: Prepare features and target
features = ['Temperature_C', 'Irradiance_W_m2', 'Solar_Efficiency', 'TEG_Efficiency']
X = df[features]  # Features
y = df['Decision']  # Target variable
print("\nFeatures (X):\n", X.head())
print("\nTarget (y):\n", y.head())

# Step 6: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("\nData split into training and testing sets:")
print(f"Training set size: {X_train.shape[0]} samples")
print(f"Testing set size: {X_test.shape[0]} samples")

# Step 7: Train a Random Forest Classifier for multi-class classification
clf = RandomForestClassifier(n_estimators=100, random_state=42)  # You can tune hyperparameters
clf.fit(X_train, y_train)
print("\nRandom Forest Classifier trained successfully!")

# Step 8: Make predictions on the test set
y_pred = clf.predict(X_test)
print("\nPredictions made on the test set.")

# Step 9: Evaluate the model
print("\nModel Evaluation:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Step 10: Use the model to make decisions for new data points
# Example: Predict the decision for a new set of conditions
new_data = pd.DataFrame({
    'Temperature_C': [26.0, 22.0, 18.0],  # Example temperatures
    'Irradiance_W_m2': [800, 1200, 900],  # Example irradiance values
    'Solar_Efficiency': [19.5, 20.0, 20.5],  # Example solar efficiency
    'TEG_Efficiency': [6.0, 6.1, 6.2]  # Example TEG efficiency
})

# Predict the decision (0, 1, or 2)
decisions = clf.predict(new_data)
print("\nDecisions for new data:")
for i, decision in enumerate(decisions):
    print(f"Data point {i+1}: Decision = {decision} (Case {decision})")