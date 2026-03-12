import os
from dotenv import load_dotenv
from apify_client import ApifyClient
from openpyxl import Workbook

load_dotenv()

# Initialize the ApifyClient with your API token
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Prepare the Actor input
run_input = {
    "urls": [
        
        "https://www.linkedin.com/search/results/content/?keywords=adya&origin=FACETED_SEARCH&mentionsOrganization=%5B%2291107261%22%5D",
        "https://www.linkedin.com/search/results/content/?keywords=shayak%20mazumder&origin=FACETED_SEARCH&mentionsMember=%5B%22ACoAAA83AZEBC4gPQP61TRTehto-qQ4TjU3IjJ8%22%5D",
    ],
    "limitPerSource": 100,
    "scrapeUntil": "2025-09-12",  # 6 months ago from the date i took the project
    "deepScrape": True,
    "rawData": False,
}

# Run the Actor and wait for it to finish
run = client.actor("Wpp1BZ6yGWjySadk3").call(run_input=run_input)

# Collect all items from the dataset
items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

if not items:
    print("No data returned from the scrape.")
else:
    # Build a unified set of column headers from all items
    all_keys = []
    seen = set()
    for item in items:
        for key in item.keys():
            if key not in seen:
                all_keys.append(key)
                seen.add(key)

    # Create the workbook and write data
    wb = Workbook()
    ws = wb.active
    ws.title = "Apify Results"

    # Write header row
    ws.append(all_keys)

    # Write data rows — convert non-string values to strings for readability
    for item in items:
        row = []
        for key in all_keys:
            value = item.get(key, "")
            if isinstance(value, (dict, list)):
                value = str(value)
            row.append(value)
        ws.append(row)

    output_file = "apify_results.xlsx"
    wb.save(output_file)
    print(f"Exported {len(items)} items to {output_file}")