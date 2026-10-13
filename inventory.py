import pandas as pd
import matplotlib.pyplot as plt

# Create a messy inventory dataset of 10 products
data = {
    "Product": [
        "Cola", "Chips", "Milk", "Juice", "Biscuits",
        "Yogurt", "Water", "Nuts", "Cheese", "Soda"
    ],
    "Category": [
        "beverages ", "SNACKS", " Dairy", "Snacks",
        "beverages", "DAIRY ", " Beverages", "snacks ",
        "dairy", "BEVERAGES"
    ],
    "Price": [
        "Rs. 1,250", "Rs. 90", "Rs. 450", "Rs. 180",
        "Rs. 120", "Rs. 200", "Rs. 50", "Rs. 350",
        "Rs. 600", "Rs. 1,800"
    ],
    "Stock": [40, 120, 60, 50, 100, 45, 150, 35, 25, 30]
}

df = pd.DataFrame(data)

# Clean category names
df["Category"] = df["Category"].str.strip().str.title()

# Remove currency prefix and thousands separators
df["Price"] = (
    df["Price"]
    .str.replace("Rs. ", "", regex=False)
    .str.replace(",", "", regex=False)
)
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# Label encoding for categories
df["Category_Code"] = df["Category"].astype("category").cat.codes

# Print the cleaned dataset
print("Cleaned Inventory Dataset:")
print(df.to_string(index=False))

print("\nCategory encoding:")
print(
    df[["Category", "Category_Code"]]
    .drop_duplicates()
    .sort_values("Category_Code")
    .to_string(index=False)
)

# Calculate average price and total stock per category
avg_price = df.groupby("Category")["Price"].mean().sort_values(
    ascending=False
)
stock_share = df.groupby("Category")["Stock"].sum()

# Create two plots side by side
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].bar(avg_price.index, avg_price.values, color="steelblue")
axes[0].set_title("Average Price by Category")
axes[0].set_xlabel("Category")
axes[0].set_ylabel("Average Price (Rs.)")
axes[0].tick_params(axis="x", rotation=20)

axes[1].pie(
    stock_share.values,
    labels=stock_share.index,
    autopct="%1.1f%%",
    startangle=90
)
axes[1].set_title("Share of Total Stock by Category")

fig.tight_layout()
fig.savefig("inventory_plots.png", dpi=150)
plt.show()

print("Saved inventory_plots.png")
