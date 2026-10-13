import pandas as pd
import matplotlib.pyplot as plt

# Create a messy student marks dataset
data = {
    "Name": [
        " ali", "SARA ", "bilal", " Ayesha",
        "HAMZA", "zain ", "Noor", " usman "
    ],
    "Marks": ["72", "85", "absent", "64", "90", "78", "81", "69"]
}

df = pd.DataFrame(data)

# Clean names by removing extra spaces and standardizing capitalization
df["Name"] = df["Name"].str.strip().str.title()

# Convert marks into numeric values; 'absent' becomes NaN
df["Marks"] = pd.to_numeric(df["Marks"], errors="coerce")

# Replace missing marks with the mean of the available marks
mean_marks = df["Marks"].mean()
df["Marks"] = df["Marks"].fillna(mean_marks)

# Display the cleaned data
print("Cleaned Student Marks:")
print(df.to_string(index=False))
print("\nMean used for absent student:", mean_marks)

# Draw the bar plot
plt.figure(figsize=(9, 5))
plt.bar(df["Name"], df["Marks"], color="steelblue")
plt.title("Student Marks")
plt.xlabel("Student Name")
plt.ylabel("Marks")
plt.ylim(0, 100)
plt.xticks(rotation=30)
plt.tight_layout()

# Save the plot in the same folder
plt.savefig("marks_bar.png", dpi=150)
plt.show()

print("Saved marks_bar.png")
