import pandas as pd
import json
import os
import logging
import re

# Logging setup
logging.basicConfig(filename="etl.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract_data(json_file="product.json"):
    """Extract raw JSON data."""
    if not os.path.exists(json_file):
        logging.error(f"File {json_file} not found.")
        return []
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def transform_data(data):
    """Clean and structure the extracted data."""
    df = pd.DataFrame(data)
    df.fillna("", inplace=True)  # Replace None with empty strings
    
    # Remove "Min. order:" from MOQ
    df["MOQ"] = df["MOQ"].astype(str).str.replace(r"Min\. order:\s*", "", regex=True)
    df["MOQ"] = df["MOQ"].apply(lambda x: "0" if x.strip() == "" else x) 

    
    # Process price column
    def process_price(price):
        """Extract lowest and highest price from price range."""
        if not price:
            return "", ""
        prices = re.findall(r"\d+\.\d+", price)  # Extract decimal numbers
        if len(prices) == 1:
            return prices[0], prices[0]  # Single price
        elif len(prices) > 1:
            return prices[0], prices[-1]  # Lowest & highest price
        return "", ""

    df["Lowest Price ($)"], df["Highest Price ($)"] = zip(*df["price"].apply(process_price))


    # Reorder columns (Lowest & Highest Price before URL)
    column_order = ["name", "Lowest Price ($)", "Highest Price ($)", "MOQ", "url"]
    df = df[column_order]

    return df
def load_data_to_excel(df, filename="cleaned_product.xlsx"):
    """Save the transformed data into Excel with clickable URLs."""
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Products")

        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets["Products"]

        # Apply hyperlink formatting to the URL column
        for row_idx, cell in enumerate(worksheet["E"], start=2):  # Assuming URL is in column E
            if cell.value:
                cell.hyperlink = cell.value
                cell.style = "Hyperlink"  # Makes it look clickable

    logging.info(f"Data successfully saved to {filename}")
    print(f"Data successfully saved to {filename}")

    # Run ETL
if __name__ == "__main__":
    raw_data = extract_data()
    if raw_data:
        transformed_df = transform_data(raw_data)
        load_data_to_excel(transformed_df)
        print("ETL Process Completed: Data cleaned and saved as cleaned_product.csv")
