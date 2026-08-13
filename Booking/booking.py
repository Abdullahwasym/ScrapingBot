import Booking.constant as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import logging
import sqlite3



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)


class BookingBot(webdriver.Chrome):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        super().__init__(options=chrome_options) 
        self.maximize_window()
        self.implicitly_wait(15)
        self.connection = self.init_db()

    def init_db(self):
        connection=sqlite3.connect("Booking_data.db")
        cursor=connection.cursor()
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS hotels(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    address TEXT,
                    certificate TEXT,
                    rating TEXT,
                    price TEXT,
                    link TEXT UNIQUE
                )
        """)
        connection.commit()
        return connection

    def land_first_page(self):
        self.get(const.BASE_URL)
    
    
    def remove_label(self):
        try:
            btn = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Dismiss sign-in info."]')
            btn.click()
            logging.info("Sign-in popup dismissed.")
        except NoSuchElementException:
            logging.info("No sign-in popup found. Continuing...")
        
               
    def change_currency(self,currency=None):
        currency_element=self.find_element(By.CSS_SELECTOR,'button[data-testid="header-currency-picker-trigger"]')
        currency_element.click()
        xpath_selector = f'//button[@data-testid="selection-item" and .//*[contains(text(), "{currency}")]]'
        button = self.find_element(By.XPATH, xpath_selector)
        button.click()
        
        
    def place_to_go(self, place_to_go):
        
        search_destination = WebDriverWait(self, 5).until(
            EC.element_to_be_clickable((By.ID, 'searchbox-horizontal-destination-input'))
        )
        
        search_destination.click()
        search_destination.send_keys(place_to_go)
        time.sleep(2)
        get_location=self.find_element(By.CSS_SELECTOR,'li[id="autocomplete-result-0"]')
        get_location.click()
    
    
    def select_dates(self,check_in_date,check_out_date):
        
        check_in_button=self.find_element(By.CSS_SELECTOR,f'span[data-date="{check_in_date}"]')
        check_in_button.click()

        check_out_button=self.find_element(By.CSS_SELECTOR,f'span[data-date="{check_out_date}"]')
        check_out_button.click()
        
    
    # helper function:-
    def select_adult_and_childs(self, element_id, target):
        target = int(target)
        
        WebDriverWait(self, 3).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        
        while True:
            value_str = self.find_element(By.ID, element_id).get_attribute('value')
            
            if value_str is None:
                value_str = "1" 
                
            current = int(value_str)
            
            if target > current:
                increase = self.find_element(By.XPATH, f'//input[@id="{element_id}"]/following-sibling::button[2]')
                increase.click()
            elif target < current:
                decrease = self.find_element(By.XPATH, f'//input[@id="{element_id}"]/following-sibling::button[1]')
                decrease.click()
            else:
                break
                
    
    def select_person(self, total_adults, total_child,total_rooms):
    
        
        occupancy_btn = self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]')
        occupancy_btn.click()
        
        self.select_adult_and_childs('group_adults', total_adults)
        self.select_adult_and_childs('group_children', total_child)
        self.select_adult_and_childs('no_rooms', total_rooms)
        
    
    def search_results(self):
        search_button=self.find_element(By.CSS_SELECTOR,'button[type="submit"]')
        search_button.click()
    
    
    def save_to_db(self,hotel):
        cursor=self.connection.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO hotels(name, address, certificate, rating, price, link) VALUES (?, ?, ?, ?, ?, ?)
        """,(hotel["Name"],hotel["Address"],hotel["Sustainability certification"],hotel["Price"],
             hotel["Rating"],hotel["Link"])
        )
            
        self.connection.commit()
        
        
    def extract_data(self):
        Data = []
        
        WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="property-card"]'))
        )
        time.sleep(3)
        self.implicitly_wait(0)
        
        seen = set()
        
        while True:
            card_container = self.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
            logging.info(f"Total hotels found: {len(card_container)}")
            previous_length = len(Data)
            logging.info(f"Previous Length: {previous_length}")
            
            for card in card_container:
                    
                logging.debug("Extracting Data......")
                try:
                    link_element = card.find_element(By.CSS_SELECTOR, 'a[data-testid="property-card-desktop-single-image"]')
                    link = link_element.get_attribute('href')
                except NoSuchElementException:
                    link = "N/A"

                dedupe_key = link.split("?")[0]

                if dedupe_key in seen:
                    continue

                seen.add(dedupe_key)
                
                try:
                    name_element = card.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]')
                    name = name_element.text
                except NoSuchElementException:
                    name = "N/A"
                    
                try:
                    address_element = card.find_element(By.CSS_SELECTOR, 'span[data-testid="address-link"]')
                    address = address_element.text
                except NoSuchElementException:
                    address = "N/A"
                    
                try:
                    certificate_element = card.find_element(By.XPATH, './/span[contains(text(), "Sustainability certification")]')
                    certificate = certificate_element.text
                except NoSuchElementException:
                    certificate = "No"
                    
                try:
                    rating_element = card.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"]>div[aria-hidden="true"]')
                    rating = float(rating_element.text)
                except NoSuchElementException:
                    rating = "No"
                    
                try:
                    price_element = card.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]')
                    price = price_element.text
                except NoSuchElementException:
                    price = "No"
                    
                data_dict={
                    "Name": name,
                    "Address": address,
                    "Sustainability certification": certificate,
                    "Price": price,
                    "Rating": rating,
                    "Link": link
                }
                self.save_to_db(data_dict)
                Data.append(data_dict)
            
            logging.info("Scrolling to load more........")       
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            try:
                load_more_btn = WebDriverWait(self, 2).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, './/button[.//span[contains(text(),"Load more results")]]')
                    )
                )
                logging.info("Button Found.....")
                load_more_btn.click()
                time.sleep(4)
            except:
                logging.info("No button Found")
                pass
            
            new_length = len(Data)
            logging.info(f"New Length: {new_length}")
            if previous_length == new_length:
                logging.info("Successfully Scraped all the data.....")
                break
                
        logging.info("Scraped Successfully!")   
        
        df = pd.DataFrame(Data)
        df.to_excel("Data.xlsx", index=False)
        logging.info("File Saved!")
        self.connection.close()