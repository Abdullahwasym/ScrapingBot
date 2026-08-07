from Booking.booking import BookingBot
from selenium import webdriver
import argparse
import time


def parse_args():
    parser = argparse.ArgumentParser(description="Booking.com Hotel Scraper")

    parser.add_argument("--city", default="New York",
                         help="Destination city to search (default: New York)")
    parser.add_argument("--checkin", default="2026-08-19",
                         help="Check-in date, format YYYY-MM-DD (default: 2026-08-19)")
    parser.add_argument("--checkout", default="2026-09-10",
                         help="Check-out date, format YYYY-MM-DD (default: 2026-09-10)")
    parser.add_argument("--currency", default="USD",
                         help="Currency code, e.g. USD, EUR, PKR (default: USD)")
    parser.add_argument("--adults", type=int, default=1,
                         help="Number of adults (default: 1)")
    parser.add_argument("--children", type=int, default=0,
                         help="Number of children (default: 0)")
    parser.add_argument("--rooms", type=int, default=1,
                         help="Number of rooms (default: 1)")

    return parser.parse_args()


def main():
    args = parse_args()

    bot = BookingBot()
    bot.land_first_page()
    bot.remove_label()
    bot.change_currency(args.currency)
    bot.place_to_go(args.city)
    bot.select_dates(args.checkin, args.checkout)
    bot.select_person(args.adults, args.children, args.rooms)
    bot.search_results()
    bot.extract_data()
    time.sleep(5)
    bot.quit()


if __name__ == "__main__":
    main()