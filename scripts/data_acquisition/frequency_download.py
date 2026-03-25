
import os
import requests
import re
import calendar
from urllib.parse import urlparse

API_URL = "https://api.neso.energy/api/3/action/datapackage_show"
DATASET_ID = "system-frequency-data"

START_YEAR = 2020
END_YEAR = 2025
END_MONTH = 9

OUTPUT_DIR = "data/raw/system_frequency"


def extract_year_month(title: str):
    m = re.search(r"([A-Za-z]+)\s+(\d{4})", title)
    if m:
        month_name = m.group(1)
        year = int(m.group(2))
        try:
            month = list(calendar.month_name).index(month_name)
            return year, month
        except ValueError:
            pass

    m = re.search(r"(\d{4})-(\d{2})", title)
    if m:
        return int(m.group(1)), int(m.group(2))

    return None, None


def fetch_resources():
    response = requests.get(API_URL, params={"id": DATASET_ID})
    response.raise_for_status()
    return response.json()["result"]["resources"]


def filter_resources(resources):
    selected = []

    for r in resources:
        if r.get("format", "").upper() != "CSV":
            continue

        title = r.get("title", "")
        year, month = extract_year_month(title)

        if year is None or month is None:
            continue

        if (
            (year > START_YEAR or (year == START_YEAR and month >= 1))
            and (year < END_YEAR or (year == END_YEAR and month <= END_MONTH))
        ):
            selected.append((r, year, month))

    return sorted(selected, key=lambda x: (x[1], x[2]))


def download_file(url, output_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    resources = fetch_resources()
    print(f"Total resources found: {len(resources)}")

    selected = filter_resources(resources)
    print(f"Filtered resources (Jan {START_YEAR} – Sep {END_YEAR}): {len(selected)}")

    for r, year, month in selected:
        url = r["path"]
        filename = os.path.basename(urlparse(url).path)
        output_path = os.path.join(OUTPUT_DIR, filename)

        if os.path.exists(output_path):
            print(f"Skipping existing file: {filename}")
            continue

        print(f"Downloading {calendar.month_name[month]} {year} -> {filename}")
        download_file(url, output_path)

    print("Download completed.")


if __name__ == "__main__":
    main()