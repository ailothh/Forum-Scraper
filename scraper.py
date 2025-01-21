import sqlite3
import requests
import time
import re
from bs4 import BeautifulSoup

# Initialize variables
test = False
useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
timeout = 0
cookie_file = "cookies.txt"

# Create a session object for handling cookies
session = requests.Session()
session.headers.update({"User-Agent": useragent})

# Save cookies to a file in a readable format
def save_cookies(session, cookie_file):
    try:
        print(f"save_cookies function called for file: {cookie_file}")  # Debug
        with open(cookie_file, "w") as f:
            for cookie in session.cookies:
                cookie_str = f"{cookie.name}={cookie.value}\n"
                f.write(cookie_str)
                print(f"Saving cookie: {cookie_str.strip()}")  # Debug
        print("Cookies saved successfully.")
    except Exception as e:
        print(f"Error saving cookies: {e}")

# Load cookies from the file if it exists
def load_cookies(session, cookie_file):
    try:
        with open(cookie_file, "r") as f:
            cookies = f.readlines()
            print("Loading cookies from file:")
            for cookie in cookies:
                print(cookie.strip())  # Debug
                name, value = cookie.strip().split("=")
                session.cookies.set(name, value)
        print("Cookies loaded successfully.")
    except FileNotFoundError:
        print("No cookies file found. Starting fresh.")

# Perform login and save cookies
def login_and_save_cookies(url, login_data):
    try:
        response = session.post(url, data=login_data)
        if response.status_code == 200:
            print("Logged in successfully.")
            print("Cookies after login:", session.cookies.get_dict())  # Debug
            save_cookies(session, cookie_file)  # Save cookies after login
        else:
            print(f"Login failed. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error during login: {e}")

# **First Action: Save Initial Cookies**
save_cookies(session, cookie_file)

# Load cookies initially if the file exists
load_cookies(session, cookie_file)

# If cookies are empty, perform login and save cookies
if not session.cookies:
    print("Session cookies are empty. Logging in to fetch new cookies...")
    login_url = ""  # Replace with actual login URL
    login_data = {
        "username": "",  # Replace with actual login data
        "password": "",  # Replace with actual login data
    }
    login_and_save_cookies(login_url, login_data)

# **Explicit Call to save_cookies After Loading**
save_cookies(session, cookie_file)

# Your scraping logic starts here...
link_pattern = r'<a\s+[^>]*?href="(https?://[^\s"]*upload[^"]*)".*?>.*?</a>'
con = sqlite3.connect("database.db") # create database
cur = con.cursor()

# Define the scraping and processing function
def scrape_page_and_process_links(url, session, cookie_file, cur, con):
    try:
        print(f"Fetching: {url}")
        r = session.get(url)
        
        # Save cookies after fetching the main page (only once)
        save_cookies(session, cookie_file)
        
        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Extract username using the specific path
        # Find all the table rows in the second table
        rows = soup.select('table:nth-of-type(2) tbody tr')

        # Loop through each row and get the username from the fourth td (href)

        # Loop through each row and get the username from the fourth td
        for row in rows:
            # First, try to find the <a> tag in the fourth <td>
            td_element = row.select_one('td:nth-of-type(4) a')
            
            if td_element:
                # If an <a> tag is found, get the username from the text
                username = td_element.get_text(strip=True)
            else:
                # If no <a> tag is found, check for a <span> tag in the same <td>
                span_element = row.select_one('td:nth-of-type(4) span')
                
                if span_element:
                    # If a <span> tag is found, set the username to "Anonymous"
                    username = "Anonymous"
                else:
                    # If neither <a> nor <span> tag is found, set it to "Unknown"
                    username = "Unknown"
            
            print(username)  # Or store the username in a list or process further
        # Extract links using the pattern
        links = re.findall(link_pattern, r.text)
        
        for link in links: # replace with links
            if link.rstrip() in {
                "",
                "",
                "",
                "",
            }:
                continue  # Skip unwanted links
            
            # Check if the link already exists in the database
            cur.execute("SELECT link FROM users WHERE link=?", (link,))
            existing_link = cur.fetchone()
            if existing_link is None:  # If the link doesn't exist, process it
                try:
                    # Fetch the link page
                    r = session.get(link)
                    
                    # Extract content from the page
                    soup = BeautifulSoup(r.text, 'html.parser')
                    data = soup.get_text(strip=True)
                    
                    # Save data to the database
                    print(f"username {type(username)}, link {type(link)}, data {type(data)}")
                    cur.execute("INSERT INTO users (username, link, data) VALUES (?, ?, ?)", (username, link, data))
                    con.commit()
                    print(f"{username} added to database")
                except Exception as e:
                    print(f"Error processing link {link}: {e}")
                    
    except Exception as e:
        print(f"Error fetching the page {url}: {e}")

# Iterate through pages
for i in range(1, 500):# replace with link
    url = f"{i}"
    scrape_page_and_process_links(url, session, cookie_file, cur, con)
    time.sleep(timeout)
