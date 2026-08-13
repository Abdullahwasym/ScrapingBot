# Booking.com Hotel Scraper – Automated Bot

A Python-based web scraper that uses Selenium to automate hotel searches on Booking.com. It handles pop-ups, sets search parameters, scrolls through dynamic content, and saves hotel data in real-time.

## How It Works

1. **Automated Navigation:** Opens a Chrome browser, navigates to Booking.com, and automatically dismisses sign-in pop-ups.
2. **Search Configuration:** Automates the selection of currency, destination, check-in/check-out dates, and guest/room quantities.
3. **Dynamic Scraping:** Scrolls through the page to trigger lazy-loaded hotel cards and clicks the "Load more results" button until all listings are displayed.
4. **Crash-Proof Saving:** Saves each hotel to a local **SQLite database** in real-time as it scrapes. If the browser crashes or gets blocked, all previously scraped data is perfectly safe.
5. **Data Export:** Once scraping is complete, the data is exported to a clean Excel file.

## Features

- **Extracted Data:** Hotel Name, Address, Sustainability Certification, Rating, Price, and direct Link.
- **Real-Time Database Storage:** Uses SQLite (`INSERT OR IGNORE`) to save data on the fly and prevent duplicate entries based on the URL.
- **Robust Error Handling:** Uses `WebDriverWait` and `try-except` blocks to handle missing elements gracefully without breaking the loop.

## Tech Stack

- Python 3
- Selenium (Browser Automation)
- SQLite3 (Real-time Database)
- pandas / openpyxl (Excel Export)

## Project Structure

```text
BookingScraper/
├── .gitignore
├── main.py (or booking_bot.py)
├── Booking/
│   └── constant.py
├── requirements.txt
└── README.md