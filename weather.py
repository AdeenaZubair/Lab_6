import pandas as pd
import matplotlib.pyplot as plt

# Create a messy 15-day weather dataset and one duplicate row
data = {
    "Date": [
        "2026-01-01", "2026-01-02", "2026-01-03",
        "2026-01-04", "2026-01-05", "2026-01-06",
        "2026-01-07", "2026-01-08", "2026-01-09",
        "2026-01-10", "2026-01-11", "2026-01-12",
        "2026-01-13", "2026-01-14", "2026-01-15",
        "2026-01-01"
    ],
    "City": [
        " lahore", "ISLAMABAD ", "Karachi", "lahore ",
        "Islamabad", "KARACHI", "Lahore", "islamabad",
        " Karachi", "LAHORE", "Islamabad ", "karachi",
        " Lahore", "ISLAMABAD", "KARACHI ", " lahore"
    ],
    "Temperature": [
        "32C", "28C", "35C", "30C", "27C",
        "36C", "33C", "29C", "34C", "31C",
        "26C", "37C", "32C", "28C", "35C", "32C"
    ],
    "Humidity": [
        45, 60, None, 55, 65, 40, None, 58,
        48, 52, None, 35, 45, 62, 42, 45
    ],
    "Condition": [
        "sunny", " Cloudy", "RAINY ", "Sunny",
        "cloudy", " sunny ", "Rainy", "CLOUDY ",
        "Sunny", "rainy", " Cloudy ", "SUNNY",
        "cloudy", "Sunny", "rainy ", " SUNNY"
    ]
}

df = pd.DataFrame(data)

# Clean text columns
df["City"] = df["City"].str.strip().str.title()
df["Condition"] = df["Condition"].str.strip().str.title()

# Remove the C suffix and convert temperature to numeric
df["Temperature"] = (
    df["Temperature"].str.replace("C", "", regex=False)
)
df["Temperature"] = pd.to_numeric(
    df["Temperature"], errors="coerce"
)

# Convert date strings into datetime values
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Remove duplicate rows
df = df.drop_duplicates().copy()
print("Rows after dropping duplicates:", len(df))

# Fill missing humidity using the median
humidity_median = df["Humidity"].median()
df["Humidity"] = df["Humidity"].fillna(humidity_median)
print("Missing Humidity filled with median:", humidity_median)

# One-hot encode weather conditions
df_encoded = pd.get_dummies(
    df, columns=["Condition"], dtype=int
)

condition_columns = [
    col for col in df_encoded.columns
    if col.startswith("Condition_")
]

print("\nEncoded condition columns:")
print(df_encoded[condition_columns].to_string(index=False))

# Calculate correlation
correlation = df["Temperature"].corr(df["Humidity"])
print(
    "\nCorrelation (Temperature, Humidity):",
    round(correlation, 3)
)

# Count the occurrences of each weather condition
condition_counts = df["Condition"].value_counts()
print("\nCondition counts:")
print(condition_counts)

# Create a 2 x 2 dashboard
fig, axes = plt.subplots(2, 2, figsize=(12, 9))

# Plot 1: Temperature over time
axes[0, 0].plot(
    df["Date"], df["Temperature"],
    marker="o", color="steelblue"
)
axes[0, 0].set_title("Temperature Over Time")
axes[0, 0].set_xlabel("Date")
axes[0, 0].set_ylabel("Temperature (C)")
axes[0, 0].tick_params(axis="x", rotation=45)
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: Temperature vs Humidity
axes[0, 1].scatter(
    df["Temperature"], df["Humidity"],
    color="darkorange"
)
axes[0, 1].set_title("Temperature vs Humidity")
axes[0, 1].set_xlabel("Temperature (C)")
axes[0, 1].set_ylabel("Humidity (%)")
axes[0, 1].grid(True, alpha=0.3)

# Plot 3: Weather condition shares
axes[1, 0].pie(
    condition_counts.values,
    labels=condition_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
axes[1, 0].set_title("Weather Condition Shares")

# Plot 4: Temperature distribution
axes[1, 1].hist(
    df["Temperature"], bins=5,
    color="seagreen", edgecolor="white"
)
axes[1, 1].set_title("Temperature Distribution")
axes[1, 1].set_xlabel("Temperature (C)")
axes[1, 1].set_ylabel("Number of Days")

# Overall dashboard title and save
fig.suptitle("Weather Overview", fontsize=16)
fig.tight_layout()
fig.savefig("weather_dashboard.png", dpi=150)
plt.show()

print("\nSaved weather_dashboard.png")
