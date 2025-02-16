# Alibaba Scraper & ETL Pipeline

This project automates **scraping Alibaba product data**, processes the extracted data, and saves it in **Excel format**. The automation runs via **GitHub Actions** and stores the output as artifacts for easy download.

---

## Features

- Scrapes Alibaba product listings
- Cleans & transforms data (removes unnecessary text, splits price ranges)
- Saves the cleaned data as **Excel (cleaned_product.xlsx)**
- Runs automatically every 6 hours via **GitHub Actions**
- Outputs are stored in **GitHub Artifacts** for download

---

## Project Structure

```
scraper_project/
│── .github/workflows/   # GitHub Actions automation
│   └── alibaba_scraper.yml # CI/CD workflow for automation
│── alibaba_spider.py     # Alibaba scraping script (Selenium)
│── ETL.py                # Data cleaning & transformation (Pandas)
│── product.json          # Raw scraped data (temporary file)
│── cleaned_product.xlsx  # Final cleaned data (output)
│── requirements.txt      # Dependencies for the project
│── README.md             # Project documentation
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/dhanesh791/scraper.git
cd scraper
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Scraper Locally

```bash
python alibaba_spider.py
```

This generates `product.json` with raw Alibaba data.

### 4. Run the ETL Script Locally

```bash
python ETL.py
```

This processes `product.json` and saves the cleaned data in `cleaned_product.xlsx`.

---

## GitHub Actions Automation

This project is automated using **GitHub Actions**, running every 6 hours.

### How to Trigger Manually

1. **Go to GitHub → Actions**
2. **Select "Alibaba Scraper Automation"**
3. **Click "Run Workflow"**

### Download Output Files

After execution, download:

- `product.json` (raw scraped data)
- `cleaned_product.xlsx` (processed data)

**To find them:**

1. **Go to GitHub → Actions → Select latest workflow run**
2. **Scroll down to "Artifacts" section**
3. **Download `cleaned_product.xlsx`**

---

## How It Works

1. **Scraper (`alibaba_spider.py`)** → Uses **Selenium** to extract data  
2. **ETL (`ETL.py`)** → Cleans, formats, and saves data to Excel  
3. **GitHub Actions (`alibaba_scraper.yml`)** → Runs scraper & ETL every 6 hours  

---

## Dependencies

This project requires the following Python packages:

- `selenium`
- `undetected-chromedriver`
- `pandas`
- `openpyxl`
- `webdriver-manager`

Install via:

```bash
pip install -r requirements.txt
```

---

## Future Improvements

- Store data in a database (e.g., PostgreSQL, MongoDB)
- Improve anti-bot evasion for better scraping
- Add email alerts for new data updates

---

## Author

- **GitHub:** [dhanesh791](https://github.com/dhanesh791)
- **Email:** dhaneshwaran1920.gmail@example.com

Happy Scraping! Let me know if you need any modifications!
