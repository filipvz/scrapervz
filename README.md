[README.md](https://github.com/user-attachments/files/26208585/README.md)
# 🎭 Events in Varaždin

A Streamlit web application that displays cultural events and cinema schedule in Varaždin in real time.

---

## Features

- **Cultural events** — fetches events from tourism-varazdin.hr (concerts, exhibitions, festivals...)
- **Kino Gaj schedule** — displays the current film programme with descriptions
- **Calendar export** — every event or film can be added directly to Google/Apple Calendar (.ics)
- **Bilingual** — interface available in Croatian and English
- **Past event filtering** — only upcoming and current events are shown

---

## Technologies

| Library | Purpose |
|---|---|
| `streamlit` | Web interface |
| `requests` | HTTP requests |
| `beautifulsoup4` | HTML parsing |
| `uuid` | Unique ID generation for .ics files |
| `zoneinfo` | Local time (Europe/Zagreb) |

---

## Running the app

```bash
streamlit run vz_gem.py
```

The app opens at `http://localhost:8501`

---

## Code structure

```
vz_gem.py
├── dohvati_dogadaje()       # Scrapes cultural events (tourism-varazdin.hr)
├── dohvati_filmove()        # Scrapes cinema schedule (kinogaj.hr)
├── dohvati_opis_filma()     # Fetches film description from individual film page
├── generiraj_ics()          # ICS file for cultural events
├── generiraj_ics_kino()     # ICS file for films
├── datum_u_datetime()       # Date parsing (format: "15 ožu")
└── datum_kino_u_datetime()  # Date parsing (format: "15.3.")
```

---

## Cache strategy

| Data | TTL |
|---|---|
| Cultural events | 1 hour |
| Cinema schedule | 1 hour |
| Film descriptions | 24 hours |

---

## Donations

If you find this app useful, you can support the project:

[💙 paypal.me/filipvz](https://paypal.me/filipvz)

---

*Powered by Filip (20% Digital) — Version 1.0*
