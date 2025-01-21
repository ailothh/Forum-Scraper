# Website Scraping Script (Proof of Concept)
#### I do not condone the use of this script on websites without authorization. This script is intended for educational and research purposes only. 
## Overview
This script is designed to scrape an entire website and save the data into an SQL database for further processing. It is tailored to large-scale database sites that host forums or posts by users. The script extracts relevant information from the links, the data associated with them, and the username of the poster, along with the post titles.

The script uses Python's requests, BeautifulSoup, and sqlite3 libraries to fetch the pages, parse the content, and store the data in a SQLite database for later analysis. It utilizes cookies for session management and ensures that cookies are saved and loaded correctly for efficient web scraping. Specific website this is designed for is taken out and not mentioned.

## Disclaimer
Unauthorized scraping may violate the terms of service of websites, and the user assumes all responsibility for any actions taken using this tool. The script is a proof of concept and may need to be adjusted based on the structure of the target website.

## Features
Scrapes entire websites and extracts content from the links.
Saves the extracted data (including usernames and post data) into an SQL database.
Manages cookies for session persistence.
Extracts links associated with specific content and checks if they exist in the database before processing.
Handles large-scale scraping with sleep intervals between requests.
## In-progress Implementions
Live scraper

