# LinkedIn Scraper - Tech Doc & Architecture

## Overview
This local web application provides a high-quality, responsive glassmorphic UI to trigger an Apify-based LinkedIn data scraper. It retrieves posts from the past 6 months (starting around September 13, 2025) and filters the outgoing `.xlsx` to only include posts matching the names "Shayak Mazumder" or "Adya".

## Architecture

1. **Frontend (`templates/index.html`)**
   - **Vanilla HTML/CSS/JS**: Uses an advanced visual layout utilizing CSS glassmorphism (backdrop-filter, layered blurred orbs) and "prism" UI lighting effects.
   - **Interactivity**: JS handles the `POST` request to the backend API without causing a page reload. Triggers the browser's download prompt dynamically utilizing a memory blob.
   
2. **Backend Server (`flask_app.py`)**
   - **Framework**: Flask (Python).
   - **Endpoints**:
     - `GET /`: Renders the `index.html` frontend.
     - `POST /api/scrape`: Invokes the synchronous scraping procedure and streams the response file back via `send_file()`.

3. **Core Scraper Logic (`scraper.py`)**
   - **Data Fetching**: Utilizes the `apify-client` and requests the standard LinkedIn Scraper Actor.
   - **Data Processing**:
     - *Row Filtering*: Compares the item's `text` property to the keywords ("adya", "shayak") case-insensitively. Drops rows that do not match.
     - *Column Filtering*: Only packs specific keys (e.g. `url`, `text`, `likesCount`, etc.) dropping all noisy arrays and unnecessary metadata.
   - **Spreadsheet Generation**: Formats the filtered dataset using `openpyxl` into an `io.BytesIO()` memory buffer. This ensures no residual file is saved onto the server's disk, optimizing I/O.

## Operating Instructions

### Prerequisites
- Python 3.9+
- The `.env` file containing your valid `APIFY_API_TOKEN` must be present.

### How to Run
1. Install requirements (if not done already):
   ```bash
   pip install -r requirements.txt
   ```
2. Start the web server:
   ```bash
   python flask_app.py
   ```
3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```
4. Click **Initiate Scrape Sequence**. The UI will display a prism loading animation while standardizing the results. The filtered spreadsheet will download automatically.

5. loom video: https://www.loom.com/share/7f0ae50537024b4fad3be19c36872edf
