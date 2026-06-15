import mysql.connector as sql 
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

conn = sql.connect(
    host = "localhost",
    user = "root",
    password = "null",
    database = "retail"
)

print("Connected")

customers = '''
    select * from customers
'''

orders = '''
    select * from orders
'''

order_items = '''
    select * from order_items
'''

print("Data loaded")

df_customers = pd.read_sql(customers,conn)
df_orders = pd.read_sql(orders,conn)
df_order_items = pd.read_sql(order_items,conn)

print("Dataframe created")

print(df_customers.head())
print(df_orders.head())
print(df_order_items.head())


print("Null values in each dataframe")
print(df_customers.isnull().sum())
print(df_orders.isnull().sum())
print(df_order_items.isnull().sum())


print ("Data types of each dataframe")
print (df_customers.dtypes)
print (df_orders.dtypes)
print (df_order_items.dtypes)



#Feature Engineering
df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])
df_orders['shipped_date'] = pd.to_datetime(df_orders['shipped_date'])
df_orders['required_date'] = pd.to_datetime(df_orders['required_date'])



print(df_orders.dtypes)





last_purchase = (
    df_orders
    .groupby("customer_id")["order_date"]
    .max()
    .reset_index()
)

reference_date = df_orders["order_date"].max()

last_purchase["days_since_last_purchase"] = (
    reference_date - last_purchase["order_date"]
).dt.days

# Frequency: Number of unique orders per customer
frequency = (
    df_orders
    .groupby("customer_id")["order_id"]
    .nunique()
    .reset_index()
    .rename(columns={"order_id": "frequency"})
)

# Total spending, total quantity, and avg discount per customer
# Compute line item subtotal: quantity * list_price * (1 - discount)
df_order_items['subtotal'] = df_order_items['quantity'] * df_order_items['list_price'] * (1 - df_order_items['discount'])

# Merge items with orders to link back to customer_id
df_merged_items = pd.merge(df_order_items, df_orders, on='order_id', how='inner')

customer_spending = (
    df_merged_items
    .groupby("customer_id")
    .agg(
        total_spending=('subtotal', 'sum'),
        total_quantity=('quantity', 'sum'),
        avg_discount=('discount', 'mean')
    )
    .reset_index()
)

# Merge all customer features
df_features = pd.merge(last_purchase[['customer_id', 'days_since_last_purchase']], frequency, on='customer_id', how='inner')
df_features = pd.merge(df_features, customer_spending, on='customer_id', how='inner')

print("\nFeatures Dataframe Head:")
print(df_features.head())

# Features (X) and Target (y)
X = df_features[['days_since_last_purchase', 'frequency', 'total_quantity', 'avg_discount']]
y = df_features['total_spending']

# Split train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scaling features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = LinearRegression()
model.fit(X_train_scaled, y_train)
print("\nModel is Ready!")

# Predictions
y_pred = model.predict(X_test_scaled)

# Evaluation metrics
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\nModel Evaluation:")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared (R2 Score): {r2:.4f}")

# Model interpretation
print("\nModel Coefficients:")
for col, coef in zip(X.columns, model.coef_):
    print(f"{col}: {coef:.2f}")
print(f"Intercept: {model.intercept_:.2f}")