import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Generate sample time-series data
dates = pd.date_range("2023-01-01", periods=100)
values = np.cumsum(np.random.randn(100)) + 100  # cumulative sum with noise

# 2. Put data into a DataFrame
df = pd.DataFrame({"Date": dates, "Value": values})
df.set_index("Date", inplace=True)

# 3. Calculate rolling averages
df["7d_Rolling"] = df["Value"].rolling(window=7).mean()
df["30d_Rolling"] = df["Value"].rolling(window=30).mean()

# 4. Plot raw values and rolling averages
plt.figure(figsize=(10, 5))
plt.plot(df.index, df["Value"], label="Raw Data", alpha=0.5)
plt.plot(df.index, df["7d_Rolling"], label="7-Day Rolling", lw=2)
plt.plot(df.index, df["30d_Rolling"], label="30-Day Rolling", lw=2)
plt.title("Sample Data with Rolling Averages")
plt.xlabel("Date")
plt.ylabel("Value")
plt.grid(True)
plt.legend()
plt.show()
