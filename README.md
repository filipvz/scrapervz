# scrapervz[README_vz_gem.md](https://github.com/user-attachments/files/25439989/README_vz_gem.md)
# VZ GEM - Events in Varazdin

A Streamlit app that fetches and displays the latest events from the Varazdin Tourism calendar.

## What the app does
- Lets users choose the interface language: Croatian or English
- Fetches events from `https://www.tourism-varazdin.hr/kalendar-dogadanja/`
- Parses HTML and displays:
  - event title
  - date
  - time
  - location

## Tech stack
- Python 3.10+
- Streamlit
- requests
- BeautifulSoup4

# 🎭 Varaždin Events Scraper

A lightweight, real-time web application that scrapes and displays the latest events in Varaždin, Croatia. Built with Python and Streamlit, this tool provides a clean, bilingual interface to keep you updated on the city's happenings.

## 📖 About the Project

This application acts as a digital scraper that fetches data directly from the [Varaždin Tourist Board calendar](https://www.tourism-varazdin.hr/kalendar-dogadanja/). It bypasses the need for a database by extracting event titles, dates, times, and locations in real-time. It was built with a strong focus on data cleaning, robust HTML parsing, and a seamless user experience.

## 🚀 Features

* **🌍 Bilingual UI (i18n):** Fully supports both Croatian and English interfaces. The UI and scraping logic dynamically adapt to the selected language.
* **⚡ Real-time Web Scraping:** Data is fetched directly from the source at the click of a button.
* **🧹 Defensive Programming:** Robust data cleaning techniques (using `.decompose()`) ensure that hidden HTML tags and messy strings don't break the application.
* **🎨 Clean & Responsive UI:** Built with Streamlit, the application groups events into neat, readable cards optimized for both desktop and mobile viewing.

## 🛠️ Tech Stack

* **[Python 3.x](https://www.python.org/)** - Core programming language
* **[Streamlit](https://streamlit.io/)** - For building the interactive web frontend
* **[BeautifulSoup4](https://beautiful-soup-4.readthedocs.io/)** - For parsing and traversing the HTML DOM
* **[Requests](https://requests.readthedocs.io/)** - For handling HTTP requests

## ⚙️ How to Run Locally

Follow these steps to run the application on your local machine:

1. **Clone the repository** and navigate to the project folder.
2. **Install the required dependencies** (it is recommended to use a virtual environment):
   ```bash
   pip install requests beautifulsoup4 streamlit


🧠 Architecture Notes (MVP Approach)
In this version, event images are intentionally excluded. During development, it was discovered that the target website uses AJAX "lazy loading" for images. Because the requests library does not execute JavaScript, fetching images would require heavy headless browser tools (like Selenium). To keep the scraper fast, lightweight, and stable, the MVP focuses purely on textual data.
## AUTHOR
Filip (20% Digital)
