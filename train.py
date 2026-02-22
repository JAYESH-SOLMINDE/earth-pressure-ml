import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# Load correct dataset
df = pd.read_excel("data/ML_Ready_Pa_Earth_Pressure_Data.xlsx")

print("Dataset Shape:", df.shape)

# Define features and target
X = df.drop("Pa_kN_m", axis=1)
y = df["Pa_kN_m"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])

# Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

# Random Forest
rf = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

# Evaluation
def evaluate(name, y_true, y_pred):
    print(f"\n{name}")
    print("R2 Score:", r2_score(y_true, y_pred))
    print("RMSE:", np.sqrt(mean_squared_error(y_true, y_pred)))
    print("MAE:", mean_absolute_error(y_true, y_pred))

evaluate("Linear Regression", y_test, y_pred_lr)
evaluate("Random Forest", y_test, y_pred_rf)

# Feature Importance
print("\nFeature Importance (Random Forest):")
for name, importance in zip(X.columns, rf.feature_importances_):
    print(f"{name}: {importance}")

# Save model
import os

# Ensure model folder exists
os.makedirs("model", exist_ok=True)

# Save model + feature order
joblib.dump(
    {
        "model": rf,
        "features": X.columns.tolist()
    },
    "model/pa_prediction_model.pkl"
)

print("\nModel saved successfully as pa_prediction_model.pkl")

plt.figure()
plt.scatter(y_test, y_pred_rf)

# Diagonal reference line
min_val = min(y_test.min(), y_pred_rf.min())
max_val = max(y_test.max(), y_pred_rf.max())
plt.plot([min_val, max_val], [min_val, max_val], linestyle='--')

plt.xlabel("Actual Pa (kN/m)")
plt.ylabel("Predicted Pa (kN/m)")
plt.title("Actual vs Predicted Pa (Random Forest)")
plt.show()