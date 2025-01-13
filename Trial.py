import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_curve, auc
import pickle  # For saving the model
import matplotlib.pyplot as plt

# Step 1: Load the CSV file
csv_file_path = 'efficiency_data_with_irradiance.csv'  # Update this path
df = pd.read_csv(csv_file_path)

# Step 2: Preprocess the data
extreme_temperature_threshold = 80  # Set the temperature threshold for sleep state
extreme_irradiance_threshold = 1200

df['Action'] = np.where((df['Temperature_C'] > extreme_temperature_threshold) | (df['Irradiance_W_m2'] > extreme_irradiance_threshold), 1, 0)

# Add a new feature: Temp_Irrad_Product
df['Temp_Irrad_Product'] = df['Temperature_C'] * df['Irradiance_W_m2']

# Features and target variable
X = df[['Temperature_C', 'Irradiance_W_m2', 'Temp_Irrad_Product', 'Solar_Efficiency', 'TEG_Efficiency', 'Net_Efficiency']]
y = df['Action']

# Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train the Random Forest model with class weights
model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Step 5: Evaluate the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Get feature importances
print("Feature importances:", model.feature_importances_)

# Step 6: Plot ROC curve to determine threshold
y_pred_proba = model.predict_proba(X_test)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()

# Choose a threshold based on the ROC curve, for example, 0.7
threshold = 0.7
y_pred_threshold = np.where(y_pred_proba >= threshold, 1, 0)
print("Accuracy with threshold:", accuracy_score(y_test, y_pred_threshold))
print("Classification Report with threshold:\n", classification_report(y_test, y_pred_threshold))

# Step 7: Save the model using pickle
model_file_path = 'solar_panel_model.pkl'
with open(model_file_path, 'wb') as file:
    pickle.dump(model, file)
print(f"Model saved to {model_file_path}")