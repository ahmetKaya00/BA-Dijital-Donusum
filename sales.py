import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

data = {
    "TV": [230,44,17,151,180,8,57,120,100,220],
    "Radio": [67,39,45,41,10,2,20,35,15,23],
    "Newspaper":[69,45,78,20,15,10,25,14,50,20,],
    "Sales":[22,10,9,18,19,5,8,15,12,21],
}

df = pd.DataFrame(data)
print(df.head())

x = df[["TV","Radio","Newspaper"]]
y = df["Sales"]

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)

print(x_train.shape)
print(x_test.shape)

model = LinearRegression()

model.fit(x_train,y_train)

print(model.coef_)
print(model.intercept_)

y_pred = model.predict(x_test)

for gerçek, tahmin in zip(y_test,y_pred):
    print(f"Gerçek: {gerçek:.2f} -> Tahmin: {tahmin:.2f}")


plt.scatter(y_test,y_pred,color='blue')
plt.xlabel("Gercek Degerler")
plt.ylabel("Tahmin Edilen Degerler")
plt.title("Lineer Regresyon")
plt.grid(True)
plt.show()