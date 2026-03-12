# BMW Used Cars Scraper

Scrapy project that scrapes used car listings from BMW UK Approved Used Cars website and stores data in SQLite database.

## Requirements

- Python 3.10+
- Google Chrome or Chromium browser

## Installation

1. Clone the repository
```bash
git clone https://github.com/vakt159/scrapy_bmw.git
cd scrapy_bmw
```

2. Create and activate virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Install Playwright browser
```bash
playwright install chromium
```

## Running
```bash
cd cars
scrapy crawl usedcars
```
