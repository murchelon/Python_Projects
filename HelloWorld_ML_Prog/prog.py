import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

ds_vgsales = pd.read_csv("vgsales_cleaned_small3.csv", sep=";")

#ds_vgsales
X = ds_vgsales.drop(columns=["Global_Sales"])
#X
y = ds_vgsales["Global_Sales"]

X_test, X_train, y_test, y_train = train_test_split (X, y, test_size=0.3)

model = DecisionTreeClassifier()

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print(accuracy_score(y_test, predictions))

print(X)