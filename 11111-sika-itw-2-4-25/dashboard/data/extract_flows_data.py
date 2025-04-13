import calendar
import os
import re
from datetime import datetime

import fitz  # PyMuPDF
import pandas as pd


def extract_flow_from_pdf(file_name="2020.pdf", folder='limmat_flows'):
    """
    Extracts daily flow values from a PDF file and saves them to a CSV file.
    """
    pdf_path = os.path.join(folder, file_name)
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(
            f"File '{pdf_path}' does not exist. Please check the file name and path."
        )

    year = int(re.search(r'\d{4}', file_name).group(0))
    is_leap_year = calendar.isleap(year)
    # Extract year from filename
    print(
        f"📅 Year extracted from filename: {year}, is it a leap year ? : {is_leap_year}")
    print(f"📄 Extracting flows from '{pdf_path}'...")
    doc = fitz.open(pdf_path)

    # Extract all text
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    # Trim to the relevant table region
    if year == 2020:
        end_trim = -277
    elif year == 2024:
        end_trim = -100
    elif year == 2023:
        end_trim = -100
    elif year == 2022:
        end_trim = -100
    elif year == 2021:
        end_trim = -100
    to_print_full_text = full_text
    full_text = "\n".join(full_text.splitlines()[57:end_trim])

    # Extract all numeric values (integers or floats)
    all_values = re.findall(r'(?<!\d)(\d{1,3}(?:\.\d{1,2})?)(?!\d)', full_text)
    print(f"🔍 Found {len(all_values)} values")

    # nb of records per day = 14 if day is betwen 1 and 28
    # Then it is 13 if day is 29 and not leap year
    # and 12 if day is 30 or 31
    records = []
    if is_leap_year:
        if year == 2024:
            for i in range(28):
                records.append(all_values[1 + i * 14:(i + 1) * 14])
            # day 29
            records.append(all_values[1 + 28 * 14:28 * 14 + 13])
            # day 30
            records.append(
                all_values[1 + 28 * 14 + 13 + 1:28 * 14 + 13 + 13])
            # day 31
            records.append(
                all_values[1 + 28 * 14 + 13 + 14:])
        else:
            for i in range(28):
                records.append(all_values[i * 14:(i + 1) * 14])
            # day 29
            records.append(all_values[28 * 14:28 * 14 + 13 - 1])
            # day 30
            records.append(
                all_values[28 * 14 + 13 + 1:28 * 14 + 13 + 12])
            # day 31
            records.append(
                all_values[28 * 14 + 13 + 14:])
    else:
        # first fill the records with 14 values, from 1 to 28
        for i in range(28):
            records.append(all_values[i * 14 + 1:(i + 1) * 14 - 1])
        # day 29
        records.append(all_values[1 + 28 * 14:28 * 14 + 13 - 1])
        # day 30
        records.append(
            all_values[28 * 14 + 13 + 1:28 * 14 + 13 + 12])
        # day 31
        records.append(
            all_values[28 * 14 + 13 + 14:])

    for i, record in enumerate(records):
        if i >= 28:
            print(f"Record {i + 1}: {len(record)}")
            print(record)

    flows = []
    dates = []

    # print last 20 lines of full_text
    # print("Last 20 lines of full text:")
    # print("\n".join(full_text.splitlines()[-20:]))
    for i, record in enumerate(records):
        day = i + 1  # Days start at 1
        nb_skip = 0
        for month in range(1, 13):
            # print("MONTH : ", month)
            # print("NB_SKIP : ", nb_skip)
            # print("DAY : ", day)
            max_day = calendar.monthrange(year, month)[1]  # e.g., 28/29/30/31
            if day > max_day:
                nb_skip += 1
                continue  # skip invalid day
            try:
                # print(f"Record {month - 1 - nb_skip}/{len(record)}")
                flow = float(record[month - 1 - nb_skip])
                date = datetime(year, month, day)
                flows.append(flow)
                dates.append(date)
            except ValueError:
                print(f"⚠️ Skipping invalid number: {record[month - 1]}")

    # Save to DataFrame
    df = pd.DataFrame({
        "Date": dates,
        "Flow (m³/s)": flows
    })

    out_path = os.path.join(folder, f"{year}.csv")
    df.to_csv(out_path, index=False)
    print(f"✅ Extracted {len(flows)} daily flows to '{out_path}'")


if __name__ == "__main__":

    folder = 'data/limmat_flows'
    if not os.path.exists(folder):
        raise FileNotFoundError(
            f"Folder '{folder}' does not exist. Please create it and place the PDF file inside."
        )

    # List files in the folder
    files = os.listdir(folder)
    for file in files:
        if file.endswith('.pdf'):
            extract_flow_from_pdf(file_name=file, folder=folder)
        else:
            print(f"❌ Skipping non-PDF file: {file}")
