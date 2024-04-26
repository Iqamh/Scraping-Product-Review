import pandas as pd

# Read CSV File
df = pd.read_csv("shopee_reviews_benboys.csv", delimiter=";")

# Check Duplicated Data
if df.duplicated(subset=["Product Name", "Variations", "Rating", "Username", "Date", "Review"]).any():
    df.drop_duplicates(
        subset=["Product Name", "Variations", "Rating", "Username", "Date", "Review"], inplace=True)
    print("Data duplikat telah dihapus.")
else:
    print("Tidak ada data duplikat.")

# Sort By Username
df = df.sort_values(by="Username")

# Delete Data with the Value in the Review Column is None
df = df[df["Review"] != "None"]

# Change Date Column to Datetime Format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Delete Data Except 2023
df = df[df['Date'].dt.year == 2023]
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

# Save
df.to_csv("cleaned_reviews_benboys.csv", index=False, sep=";")
