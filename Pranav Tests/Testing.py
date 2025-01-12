from BinaryClassification import clf, accuracy_score, confusion_matrix, classification_report
import pandas as pd

# Step 1: Prepare test data
# Replace these values with your test data
test_data = pd.DataFrame({
    'Temperature_C': [26.0, 22.0, 100.0],  # Example temperatures
    'Irradiance_W_m2': [800, 1200, 900],  # Example irradiance values
    'Solar_Efficiency': [19.5, 20.0, 20.5],  # Example solar efficiency
    'TEG_Efficiency': [6.0, 6.1, 6.2]  # Example TEG efficiency
})

# Step 2: Make predictions using the trained model
predictions = clf.predict(test_data)

# Step 3: Interpret the output
print("\nPredictions for test data:")
for i, pred in enumerate(predictions):
    print(f"Test data point {i+1}: Decision = {pred} (Case {pred})")

# Step 4: (Optional) Evaluate performance if true labels are available
# Replace `true_labels` with the actual labels for the test data
true_labels = [2, 1, 0]  # Example true labels for the test data

if len(true_labels) == len(predictions):
    print("\nModel Performance on Test Data:")
    print("Accuracy:", accuracy_score(true_labels, predictions))
    print("Confusion Matrix:\n", confusion_matrix(true_labels, predictions))
    print("Classification Report:\n", classification_report(true_labels, predictions))
else:
    print("\nTrue labels not provided or do not match the number of predictions.")