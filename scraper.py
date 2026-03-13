import os
import io
from dotenv import load_dotenv
from apify_client import ApifyClient
from openpyxl import Workbook

load_dotenv()

USEFUL_COLUMNS = [
    "url",
    "authorUrl",
    "authorName",
    "text",
    "publishedAt",
    "likesCount",
    "commentsCount",
    "repostsCount",
]

def run_scraper_and_generate_excel():
    client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

    run_input = {
        "urls": [
            "https://www.linkedin.com/search/results/content/?keywords=adya&origin=FACETED_SEARCH&mentionsOrganization=%5B%2291107261%22%5D",
            "https://www.linkedin.com/search/results/content/?keywords=shayak%20mazumder&origin=FACETED_SEARCH&mentionsMember=%5B%22ACoAAA83AZEBC4gPQP61TRTehto-qQ4TjU3IjJ8%22%5D",
        ],
        "limitPerSource": 100,
        "scrapeUntil": "2025-09-13",
        "deepScrape": True,
        "rawData": False,
    }

    run = client.actor("Wpp1BZ6yGWjySadk3").call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    if not items:
        return None, 0

    filtered_items = []
    
    for item in items:
        text = str(item.get("text", "")).lower()
        if "adya" in text or "shayak" in text:
            # Filter columns
            filtered_item = {}
            for col in USEFUL_COLUMNS:
                val = item.get(col, "")
                if isinstance(val, (dict, list)):
                    val = str(val)
                filtered_item[col] = val
            filtered_items.append(filtered_item)
            
    if not filtered_items:
        return None, 0
            
    wb = Workbook()
    ws = wb.active
    ws.title = "Apify Results"
    
    ws.append(USEFUL_COLUMNS)
    
    for item in filtered_items:
        row = [item.get(col, "") for col in USEFUL_COLUMNS]
        ws.append(row)
        
    excel_buffer = io.BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)
    
    return excel_buffer, len(filtered_items)
