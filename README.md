# vz_gem.py

`vz_gem.py` is a Streamlit app that fetches public event data from the official Varaždin tourism calendar, displays upcoming events, and lets users download each event as an `.ics` calendar file.

## Features
- Bilingual UI: Croatian (`Hrvatski HR`) and English (`English EN`)
- Fetches events from: `https://www.tourism-varazdin.hr/kalendar-dogadanja/`
- Parses and displays event title, date, time, and location
- Filters out past events and sorts upcoming events by date
- Collapsible event cards (expander UI) for a clean, compact view
- Exports single-event `.ics` files for calendar import
- Styled header with color background (bilingual)
- Data fetch timestamp shown after each load
- Uses Streamlit caching (`@st.cache_data`) with 1-hour TTL
- Deduplicates events by title and date
- Network error handling with 10-second timeout
- Smart year resolution: always picks the next upcoming date, never a past one

## Requirements
- Python 3.11+
- streamlit
- requests
- beautifulsoup4

## Installation

```bash
pip install streamlit requests beautifulsoup4
```

## Run

```bash
streamlit run vz_gem.py
```

## How It Works
1. User selects language in the UI.
2. App sends an HTTP GET request to the Varaždin events page (timeout: 10s).
3. BeautifulSoup parses event blocks (`div.eventon_list_event`).
4. App extracts:
   - title (`span.evoet_title`)
   - day (`em.date`)
   - month (`em.month`)
   - time (`em.time`)
   - location (`span.event_location_attrs` → `data-location_name`)
5. Duplicate events (same title + date) are removed automatically.
6. Dates are converted to datetime values — the source provides no year, so the app picks the first upcoming future date across candidate years.
7. Past events are filtered out and results are sorted by date.
8. Results are rendered in collapsible expander cards.
9. Each event can be downloaded as an `.ics` file generated in memory.

## Error Handling
- If the server is unreachable or the request times out, the app returns an empty list gracefully.
- If a date cannot be parsed or no future candidate exists, a fallback value is used for ICS generation (`00000000`).

## Notes
- Source data quality depends on the structure and content of the tourism website.
- ICS export is generated as an all-day event (`VALUE=DATE`).

## Live App
https://scrapervz.streamlit.app/

## Author
Filip (20% Digital)
