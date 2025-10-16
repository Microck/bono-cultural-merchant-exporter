# Bono Cultural Merchant Exporter

A Python script that scrapes all online merchants from Spain's "Bono Cultural Joven" API and exports them to a CSV file.

This project provides a Python script designed to automatically extract a complete and up-to-date list of all online establishments participating in Spain's "Bono Cultural Joven" program. Created to overcome the limitations of the official web interface, this tool offers a fast and efficient way to get all merchant data at once for offline use.

It leverages the `requests` library to query the official API directly, bypassing slow HTML parsing. The script efficiently iterates through all available pages of results, collecting the name, website, and product categories for each merchant. A key feature is its ability to translate the raw API category codes (e.g., `PHYSICAL_SUPPORT`) into a user-friendly Spanish format. The final, clean list is then exported into a structured CSV file (`establecimientos_bono_cultural.csv`), perfect for easy searching, filtering, or data analysis.

---

## How to Use

### Prerequisites

*   Python 3.6 or newer
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Microck/bono-cultural-merchant-exporter.git
    cd bono-cultural-merchant-exporter
    ```

2.  **Install the required libraries:**
    ```bash
    pip install requests pandas
    ```

### Execution

Run the script from your terminal:
```bash
python scraper.py
```
You will see progress messages as the script fetches data from each page of the API.

### Output

Once the script finishes, a file named `establecimientos_bono_cultural.csv` will be created in the same directory. This file contains all scraped merchants with the following columns: `nombre`, `web`, and `tipos`.
