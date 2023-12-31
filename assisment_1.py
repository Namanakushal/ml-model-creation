import pandas as pd

# Load the Excel file
file_path = '/content/customer_churn_large_dataset.xlsx'
df = pd.read_excel(file_path)

print("First few rows of the dataset:")
print(df.head())

print("\nBasic statistics:")
print(df.describe())

df.dropna(inplace=True)

df

from scipy.stats import zscore
z_scores = zscore(df.select_dtypes(include=['float64']))
df = df[(z_scores < 3).all(axis=1)]

label_encoder = LabelEncoder()
categorical_columns = df.select_dtypes(include=['object']).columns
for col in categorical_columns:
    df[col] = label_encoder.fit_transform(df[col])

X = df.drop('Churn', axis=1)  # Features
y = df['Churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train, X_test, y_train, y_test )

from sklearn.preprocessing import StandardScaler

# Initialize the scaler
scaler = StandardScaler()

# Fit and transform the scaler on your features
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Initialize the model
model = LogisticRegression()

# Train the model
model.fit(X_train_scaled, y_train)

# Validate the model
y_pred = model.predict(X_test_scaled)

# Evaluate the model's performance
print("Classification Report:\n", classification_report(y_test, y_pred))

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Define the hyperparameter grid with valid penalties for the 'lbfgs' solver
param_grid = {'C': [0.1, 1, 10], 'penalty': ['l2', 'none']}

# Initialize GridSearchCV
grid_search = GridSearchCV(LogisticRegression(solver='lbfgs'), param_grid, cv=5)

# Fit the grid search to the data
grid_search.fit(X_train_scaled, y_train)

# Get the best parameters
best_params = grid_search.best_params_

# Use the best model
best_model = grid_search.best_estimator_

y_pred_best = best_model.predict(X_test_scaled)

print("Best Model Classification Report:\n", classification_report(y_test, y_pred_best))
