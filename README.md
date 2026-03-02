[README_vz_gem.md](https://github.com/user-attachments/files/25681598/README_vz_gem.md)
# vz_gem.py

`vz_gem.py` is a Streamlit app that fetches public event data from the official Varazdin tourism calendar, shows upcoming events, and lets users download each event as an `.ics` calendar file.

## Features
- Bilingual UI: Croatian (`Hrvatski HR`) and English (`English EN`)
- Fetches events from: `https://www.tourism-varazdin.hr/kalendar-dogadanja/`
- Parses and displays event title, date, time, and location
- Filters out past events and sorts upcoming events by date
- Exports single-event `.ics` files for calendar import
- Uses Streamlit caching (`@st.cache_data`) with 1-hour TTL

## Requirements
- Python 3.10+
- streamlit
- requests
- beautifulsoup4

## Installation
Install dependencies:

```bash
pip install streamlit requests beautifulsoup4
```

## Run
From the project root:

```bash
streamlit run Perplex/slike/vz_gem.py
```

## How It Works
1. User selects language in the UI.
2. App sends an HTTP GET request to the Varazdin events page.
3. BeautifulSoup parses event blocks (`div.eventon_list_event`).
4. App extracts:
   - title (`span.evoet_title`)
   - day (`em.date`)
   - month (`em.month`)
   - time (`em.time`)
   - location (`span.event_location_attrs` -> `data-location_name`)
5. Dates are converted to datetime values and filtered to keep only today/future events.
6. Results are sorted and rendered in Streamlit.
7. Each event can be downloaded as an `.ics` file generated in memory.

## Notes
- Source data quality depends on the structure/content of the tourism website.
- If a date cannot be parsed, a fallback value is used for ICS generation (`00000000`).
- ICS export is generated as an all-day event (`VALUE=DATE`).

## Author

Filip (20% Digital)

