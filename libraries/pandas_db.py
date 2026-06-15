from sqlalchemy import false
import pandas as pd
import mysql.connector as mysql

conn = mysql.connect(
    host="localhost",
    user="root",
    password="null",
    database="ecommerce"
)
print("connected successfullly...")


query = """ 
SELECT * FROM customers

"""

df = pd.read_sql(query,conn)

print("Data Loaded")
'''
print(df.head())
print(df.tail())
print(df.shape)
print(df.info())
print(df.describe())
print(df.columns)
print(df.dtypes)
'''

'''
#Coloumn Selection

print(df["customer_id"])
print(df[["customer_id","customer_city"]])
print(df[["customer_id","customer_city","customer_state"]])
'''

'''
#Row Slelection
print(df[100:110])
'''

'''
#LOC Location By Label

print(df.loc[0:5, ["customer_city", "customer_state"]])

print(df.iloc[0:5,1:3])
'''

'''
#print(df[df["customer_state"] == "SP"])

#print(df[df["customer_city"] != "franca"])

#print(df[(df["customer_city"] == "franca") & (df["customer_state"] == "SP")])

#print(df[(df["customer_city"] == "franca") | (df["customer_state"] == "RJ")])

'''



'''

#SORTING

print(
    df.sort_values(by = ["customer_city","customer_state"], ascending=[False,True])
)

'''

'''
#Unique Values
print(
    df.customer_state.unique
)
#No of unique values
print(
    df.customer_state.nunique()
)
'''


'''
#Value Counts

print(
    df.customer_state.value_counts()
)

print(df["customer_city"].value_counts().head(10))
print(df["customer_state"].value_counts(ascending=True))
print(df["customer_state"].value_counts(normalize=True))

'''


'''
#GROUP BY
print(df.groupby("customer_state"))
print(df.groupby("customer_state").size())
print(
    df.groupby("customer_state")
      .size()
      .sort_values(ascending=False)
)

'''

'''
Transform
print(df.groupby("customer_state")["customer_id"].transform("sum"))

'''

'''

def categorize_city(city):
    if city == "SP" or city == "RJ":
        return "South-East"
    elif city == "MG" or city == "ES":
        return "South-West"
    else:
        return "Other"  


print(df["customer_state"].apply(categorize_city))

'''


df.isnull().sum()