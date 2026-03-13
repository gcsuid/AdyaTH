# LinkedIn Content Automation - Project Presentation

## Agenda

1.  **Project Overview**
    *   **Objective:** Automate the extraction of LinkedIn posts specifically referencing "Adya" or "Shayak" over the past 6 months.
    *   **Goal:** Replace the manual terminal script with an intuitive, self-contained local web application.
    *   **Data Integrity:** Ensure output is free of "noise" columns (like raw JSON metadata) and strictly preserves the rows matching the keyword condition.

2.  **Architecture & Design**
    *   **Backend Engineering:** Refactored the original Apify script into a scalable Python module (`scraper.py`) to increase code reusability. Wrapped this inside a lightweight Flask server.
    *   **Frontend Aesthetics:** Designed a custom, high-end "Glassmorphism" UI using pure HTML and CSS. The design features a responsive edge-to-edge dark gradient, animated blurred orbs, and a completely custom loading indicator.
    *   **Storage Optimization:** Transitioned from writing physical `.xlsx` files to disk on the server to utilizing an in-memory byte buffer. This streams the generated Excel file directly to the user's browser for download, eliminating cleanup and storage concerns.

3.  **Demonstration of Requirements Achieved**
    *   **Requirement 1 (Interactive UI):** We built a beautiful localhost URL where anyone can simply click a button to initiate the scrape and download the results without touching code.
    *   **Requirement 2 (Noise Filtering - Columns):** We explicitly select only `url`, `authorUrl`, `authorName`, `text`, `publishedAt`, `likesCount`, `commentsCount`, and `repostsCount`. All other dataset noise is dropped.
    *   **Requirement 3 (Data Filtering - Rows):** We parse the `text` attribute of every post during extraction, ensuring that either "adya" or "shayak" is present before adding the row to the final spreadsheet.
    *   **Requirement 4 (Time Horizon):** Set the `scrapeUntil` timestamp precisely to 6 months accurately capturing the user's request context.

4.  **Workflow summary**
    1.  User clicks the glowing button on localhost.
    2.  Asynchronous JS request hits the `/api/scrape` endpoint.
    3.  Flask calls the `apify-client` scraper Actor.
    4.  The actor generates a dataset.
    5.  Python filters the dataset (by row logic, then by column definition) and assembles a Workbook using `openpyxl`.
    6.  Workbook is encoded to an openxml format and streamed as `filtered_apify_results.xlsx` to the browser.

5.  **Technical Resources**
    *   **Git Repository Initiation:** You can immediately initialize this directory as a Git repo via `git init`.
    *   **Documentation:** Technical documentation and architectural decisions are outlined in the provided `README.md`.
    *   **Test Recording:** An automated video recording demonstrating the entire flow is available in the artifacts folder.
