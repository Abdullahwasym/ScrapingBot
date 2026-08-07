from Booking.booking import BookingBot
from selenium import webdriver
import time

def main():
    bot=BookingBot()
    bot.land_first_page()
    bot.remove_label()
    bot.change_currency("USD")
    bot.place_to_go("New York")
    bot.select_dates("2026-08-19","2026-09-10")
    bot.select_person(1,0,1)
    bot.search_results()
    bot.extract_data()
    time.sleep(5)
    bot.quit()      


if __name__=="__main__":
    main()