import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

start_date = pd.Timestamp("2025-01-01")
days = 180
dates = pd.date_range(start_date,periods=days,freq="D")

companies = ["MarsLog","OrionCargo","VegaTrans"]

rows = []

for dt in dates:
    for comp in companies:
        base_delivers = 150 + 40*np.sin((dt.day_of_year/365)*2*np.pi)
        deliveries = int(np.clip(np.random.normal(base_delivers,25),80,220))

        on_time = np.clip(np.random.normal(0.9 + 0.05*np.cos(dt.day_of_year/50),0.04),0.8,0.98)
        avg_delivery_min = np.clip(np.random.normal(55-15*(on_time-0.9),6),35,75)

        distance_km = deliveries * np.random.uniform(12,25)

        fuel_l_per_100km = np.clip(np.random.normal(22-3*(on_time-0.9),2.5),18,28)

        idle_min_per_vehicles = np.clip(np.random.normal(12+120*(1-on_time),4),5,25)

        app_latency_ms = int(np.clip(np.random.normal(250+120*(1-on_time),60),120,550))
        incidents = int(np.clip(np.random.poisson(1.0+2.0*(1-on_time)),0,8))

        tickets_opened = int(np.clip(np.random.normal(deliveries*0.03,3),0,deliveries*0.1))
        tickets_resolved = int(np.clip(tickets_opened - np.random.randint(0,3),0,tickets_opened))

        csat = np.clip(np.random.normal(3.5+1.5*(on_time-0.85),0.35),1,5)
        rows.append({
            "date": dt,
            "company": comp,
            "deliveries":deliveries,
            "on_time_rate":round(on_time,4),
            "avg_delivery_min":round(avg_delivery_min,2),
            "distance_km":round(distance_km,2),
            "fuel_l_per_100km":round(fuel_l_per_100km,2),
            "idle_min_per_vehicles": round(idle_min_per_vehicles,2),
            "app_latency_ms":int(app_latency_ms),
            "incidents":incidents,
            "tickets_opened":tickets_opened,
            "tickets_resolved":tickets_resolved,
            "csat":round(csat,2)
        })
df = pd.DataFrame(rows)

df["late_deliveries"] = (df["deliveries"] * (1-df["on_time_rate"])).round().astype(int)
df["fuel_total_liters"] = (df["distance_km"] / 100.0)*df["fuel_l_per_100km"]
df["fuel_per_delivery_l"] = df["fuel_total_liters"] / df["deliveries"]

df.to_csv("smart.csv",index=False)

df["week"] = df["date"] - pd.to_timedelta(df["date"].dt.weekday,unit="D")

weekly = (
    df.groupby(["week","company"])
    .agg(
        deliveries=("deliveries","sum"),
        on_time_rate=("on_time_rate","mean"),
        avg_delivery_min=("avg_delivery_min","mean"),
        fuel_l_per_100km=("fuel_l_per_100km","mean"),
        fuel_per_delivery_l=("fuel_per_delivery_l","mean"),
        csat=("csat","mean"),
        incidents=("incidents","sum")
    )
    .reset_index()
)

plt.figure()
for comp in companies:
    subset = weekly[weekly["company"]==comp]
    plt.plot(subset["week"],subset["avg_delivery_min"],label=comp)
plt.title("Haftalik Ortalama Teslim Suresi(dakika)")
plt.xlabel("Hafta")
plt.ylabel("Dakika")
plt.legend()
plt.savefig("haftalik_teslim.png")
plt.show

company_csat = df.groupby("company")["csat"].mean().reset_index()
plt.figure()
plt.bar(company_csat["company"],company_csat["csat"])
plt.title("Sirket Bazli Ortalama CSAT")
plt.xlabel("Sirket")
plt.ylabel("CSAT(1-5)")
plt.savefig("csat.png")
plt.show

plt.figure()
plt.scatter(df["on_time_rate"],df["fuel_l_per_100km"])
plt.title("On Time Oranı vs Yakıt Tüketimi")
plt.xlabel("On-Time")
plt.ylabel("L/100km")
plt.savefig("cson_timeat.png")
plt.show