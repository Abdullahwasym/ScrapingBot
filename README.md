# Booking.com Hotel Data Scraper – Automated

An automated web scraping bot built with **Python** and **Selenium** that searches Booking.com for hotels based on custom parameters (destination, dates, guests, currency) and extracts structured hotel data into a clean Excel file.

## Features

- Automates the full search flow: dismisses sign-in popup, sets currency, enters destination, selects check-in/check-out dates, and configures guests/rooms
- Handles dynamic content loading via infinite scroll and "Load more results" button detection
- Deduplicates listings to avoid repeated entries across scroll loads
- Extracts for every hotel:
  - Name
  - Address
  - Sustainability certification (Yes/No)
  - Price
  - Rating
  - Direct booking link
- Saves results to `Data.xlsx`
- Full run logging to `app.log` for debugging and monitoring
- Configurable via command-line arguments — no code changes needed to search a different city or date range

## Tech Stack

- Python 3
- Selenium (Chrome WebDriver)
- pandas (Excel export)

## Project Structure

```
BOT/
├── Booking/
│   ├── __init__.py
│   ├── booking.py       # BookingBot class — all automation logic
│   └── constant.py      # Base URL and constants
├── run.py               # Entry point with CLI arguments
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/Abdullahwasym/ScrapingBot.git
cd ScrapingBot
pip install -r requirements.txt
```

Requires Google Chrome installed (Selenium controls it via ChromeDriver).

## Usage

Run with default parameters (New York, 2026-08-19 to 2026-09-10, USD, 1 adult):

```bash
python run.py
```

Run with custom parameters:

```bash
python run.py --city "Dubai" --checkin 2026-09-01 --checkout 2026-09-05 --currency EUR --adults 2 --children 1 --rooms 1
```

### Available arguments

| Argument      | Default      | Description                     |
|---------------|--------------|----------------------------------|
| `--city`      | New York     | Destination city to search       |
| `--checkin`   | 2026-08-19   | Check-in date (YYYY-MM-DD)       |
| `--checkout`  | 2026-09-10   | Check-out date (YYYY-MM-DD)      |
| `--currency`  | USD          | Currency code (USD, EUR, PKR...) |
| `--adults`    | 1            | Number of adults                 |
| `--children`  | 0            | Number of children               |
| `--rooms`     | 1            | Number of rooms                  |

## Output

Results are saved to `Data.xlsx` with columns: `Name`, `Address`, `Sustainability certification`, `Price`, `Rating`, `Link`.

A single run has been tested to successfully extract 600+ hotel listings for a single search.

## Notes

- Booking.com's page structure may change over time, which can require selector updates in `booking.py`.
- This project was built for demonstration/portfolio purposes. Please respect target websites' terms of service when scraping.
