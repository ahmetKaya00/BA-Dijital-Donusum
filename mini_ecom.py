import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

users = pd.DataFrame({
    "user_id":[1,2,3,4],
    "name": ["Ali","Ayşe","Mehmet","Zeynep"],
    "city": ["İstanbul","Ankarta",np.nan,"İzmir"]
})

orders = pd.DataFrame({
    "order_id":[101,102,103,104,105],
    "user_id":[1,1,2,3,4],
    "order_date": pd.to_datetime(["2025-01-10","2025-02-12","2025-02-20","2025-03-10","2025-03-15"]),
    "amount":[250.0,np.nan,900.0,120.0,300.0],
    "payment_method": ["KK","Havale","KK",np.nan,"KK"]
})

returns = pd.DataFrame({
    "order_id":[103,105],
    "is_returned": [True,np.nan]
})

users["city"] = users["city"].fillna("Bilinmiyor")

orders["amount"] = pd.to_numeric(orders["amount"],errors="coerce").fillna(orders["amount"].median())

orders["payment_method"] = orders["payment_method"].fillna(orders["payment_method"].mode()[0])

returns["is_returned"] = returns["is_returned"].fillna(False)

df = orders.merge(users, on="user_id", how="left").merge(returns, on="order_id",how="left")

df["is_returned"] = df["is_returned"].fillna(False)

df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()

net_revenue = df.loc[~df["is_returned"],"amount"].sum()

return_rate = df["is_returned"].mean()

print(f"Net Ciro: {net_revenue:.2f} TL | İade Oranı: {return_rate:.0%}")

m = df.loc[~df["is_returned"]].groupby("month")["amount"].sum()

m.plot(marker="o", title="Aylık Net Ciro")
plt.xlabel("Ay")
plt.ylabel("TL")

plt.tight_layout()
plt.savefig("aylik_cire.png")
