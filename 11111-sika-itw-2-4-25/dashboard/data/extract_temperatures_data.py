import os
import re
from datetime import datetime, timedelta

import fitz  # PyMuPDF
import pandas as pd


def extract_temp_from_pdf(file_name="0951.pdf", folder='limmat_temperatures'):
    """
    Extracts temperature data from a PDF file and saves it to a .csv file
    """
    pdf_path = os.path.join(folder, file_name)
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(
            f"File '{pdf_path}' does not exist. Please check the file name and path."
        )
    print(f"📄 Extracting temperatures from '{pdf_path}'...")
    doc = fitz.open(pdf_path)

    # Extract all text
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    # Extract repeated values like 6.9\n6.9
    pattern = r'(\d{1,2}\.\d)\s*\n\s*\1'
    all_values = re.findall(pattern, full_text)

    print(
        f"🔍 Found {len(all_values)} repeated values (may include monthly summaries)")

    # filename is year.pdf
    # get year from filename
    year = int(re.search(r'\d{4}', file_name).group(0))
    print(f"📅 Year extracted from filename: {year}")

    # define days in month for leap year, and for a non-leap year
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else:
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Iterate and collect only the daily values
    temperatures = []
    index = 0
    increment = 10 if year != 2024 else 3

    for days in days_in_month:
        temperatures.extend(all_values[index:index + days])  # Add daily values
        index += days + increment  # Skip the 3 monthly summary values

    # Create date range
    start_date = datetime(year, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(len(temperatures))]

    # Save to DataFrame
    df = pd.DataFrame({
        "Date": dates,
        "Temperature (°C)": temperatures
    })

    out_path = os.path.join(folder, f"{year}.csv")
    df.to_csv(out_path, index=False)
    print(
        f"✅ Extracted {len(temperatures)} daily temperatures to '{out_path}'")


if __name__ == "__main__":

    folder = 'limmat_temperatures'
    if not os.path.exists(folder):
        raise FileNotFoundError(
            f"Folder '{folder}' does not exist. Please create it and place the PDF file inside."
        )

    # list files
    files = os.listdir(folder)
    for file in files:
        if file.endswith('.pdf'):
            extract_temp_from_pdf(file_name=file, folder=folder)
        else:
            print(f"❌ Skipping non-PDF file: {file}")
