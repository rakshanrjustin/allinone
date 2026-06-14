import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

df = pd.DataFrame({
    'Age':[25,30,None,45,22,35,29,1000,28,31],
    'Salary':[30000,45000,50000,None,25000,70000,60000,9999999,40000,48000],
    'Experience':[1,5,4,15,None,10,6,100,3,5],
    'Department':['IT','HR','IT',None,'Sales','IT','HR','Unknown','Sales','HR'],
    'Promoted':[0,1,1,1,0,1,1,1,0,1]
})




#Data Inspection
#print(df.info())
#print(df.isnull().sum())

#OUTLIERS
#df.boxplot(column="Age")
#plt.show()

#df["Age"].plot(kind="bar")
#plt.show()

#print(df.iloc[0:11])
#print(df.describe())
#print(df["Age"].sort_values(ascending = False))







#Data Cleaning
#Step1: Handle Outliers

df = df[df["Age"] != 1000]
print("Outlier Deleted!")

print(df.isnull().sum())

#Step2: Handle Missing Values

df["Age"] = df["Age"].fillna(df["Age"].mean())
df["Salary"] = df["Salary"].fillna(df["Salary"].median())
df["Experience"] = df["Experience"].fillna(df["Experience"].median())
df["Department"] = df["Department"].fillna(df["Department"].mode()[0]) 
print(df.isnull().sum())


#Remove Duplicates
print(df.duplicated().sum())

#Data Encoding

df = pd.get_dummies(df,columns=["Department"])
print(df.head())





#TRAINING

X = df.drop("Promoted", axis=1)
y = df["Promoted"]

X_train,X_test,y_train,y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

#SCALLING

scaller =StandardScaler()
X_train = scaller.fit_transform(X_train)
X_test = scaller.transform(X_test)

#MODEL SELECTION

model = SVC()
model.fit(X_train,y_train)
print("Model is Ready!")

#PREDICTION

prediction = model.predict(X_test)
print(prediction)
print(y_test)


#EVALUATION

accuracy = accuracy_score(y_test,prediction)
print("Accuracy",accuracy)


print(confusion_matrix(y_test, prediction))
print(classification_report(y_test, prediction))