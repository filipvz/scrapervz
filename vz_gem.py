import streamlit as st  
import requests
from bs4 import BeautifulSoup
import uuid
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo

URL_KINO_GAJ = "https://www.kinogaj.hr/raspored.html"

MJESECI={
    "sij":"01","vel":"02","ožu":"03",
    "tra":"04","svi":"05","lip":"06",
    "srp":"07","kol":"08","ruj":"09",
    "lis":"10","stu":"11","pro":"12" #EN fallback
}
MJESECI_OBRNUTO={v:k for k,v in MJESECI.items()}

JEZICI={
    "Hrvatski HR":{
        "url":"https://www.tourism-varazdin.hr/kalendar-dogadanja/",
        "naslov":"Događaji u Varaždinu",
        "opis":"Dobrodošli u našu aplikaciju koja prikazuje događaje u Varaždinu",
        "gumb":" 🏛️ Dohvati najnovije kulturne događaje u gradu",
        "ucitavanje":"Dohvaćanje događaja...",
        "Uspjeh":"Pronađeno je {} događaja.",
        "greska":"Nema dostupnih događaja.",
        "lbl_datum":"Datum",
        "lbl_vrijeme":"Vrijeme",
        "lbl_lokacija":"Lokacija",
        "lbl_naslov":"Naslov",
        "dohvaceno":"Podaci dohvaćeni u ",
        "gumb_kino": "🎬 Kino Gaj - raspored",
        "ucitavanje_kino": "Dohvaćanje filmova...",          
        "uspjeh_kino": "Pronađeno je {} filmova.",
        "greska_kino": "Nema dostupnih filmova."

        
    },
    "English EN":{
        "url":"https://www.tourism-varazdin.hr/kalendar-dogadanja/",
        "naslov":"Events in Varaždin",
        "opis":"Welcome to our application that displays events in Varaždin",
        "gumb":" 🏛️ Get latest events in town",
        "ucitavanje":"Loading events...",
        "Uspjeh":"Found {} events.",
        "greska":"No events available.",
        "lbl_datum":"Date",
        "lbl_vrijeme":"Time",
        "lbl_lokacija":"Location",
        "lbl_naslov":"Title",
        "dohvaceno":"Events loaded at ",
        "gumb_kino": "🎬 Kino Gaj - schedule",
        "ucitavanje_kino": "Getting movies...",          
        "uspjeh_kino": "{} movies were found.",
        "greska_kino": "No movies available."
        
    }
} 

@st.cache_data(ttl=3600)
def dohvati_dogadaje(url):
    
    
    headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    try:
        response=requests.get(url,headers=headers,timeout=10)#Zahtjev za server, 10 sec za server
    except requests.exceptions.RequestException: 
        return[]
    
    dogadaji_lista=[]
    vidjeni=set()
    if response.status_code==200: #status kod 200 ok provjera servera
        
        soup=BeautifulSoup(response.text,"html.parser") #Dohvaćanje sadržaja stranice
        dogadaji_html=soup.find_all("div",class_="eventon_list_event")
        
    
        for dogadaj in dogadaji_html:
            naslov_element=dogadaj.find('span',class_='evoet_title')
            dan_element=dogadaj.find('em',class_='date')
            mjesec_element=dogadaj.find('em',class_='month')
            vrijeme_element=dogadaj.find('em',class_='time')
            lokacija_element=dogadaj.find('span',class_='event_location_attrs')          
            
            if naslov_element:
                naslov=naslov_element.text.strip()
                dan=dan_element.text.strip()if dan_element else "??"
                mjesec=mjesec_element.text.strip()if mjesec_element else "??"
                vrijeme_element=dogadaj.find('em',class_='time')
                if vrijeme_element:
                    uljez=vrijeme_element.find('i')
                    if uljez:
                        uljez.decompose()
                    vrijeme=vrijeme_element.text.strip()
                else:
                    vrijeme="??"
                lokacija=lokacija_element.get('data-location_name') if lokacija_element else "Nepoznata lokacija"
                                
                #Kreiranje riječnika i liste

                dogadaj_podaci={
                    "naslov":naslov,
                    "datum":f"{dan} {mjesec}",
                    "vrijeme":vrijeme,
                    "lokacija":lokacija,
                    
                }
                kljuc=(naslov,f"{dan} {mjesec}")
                if kljuc not in vidjeni:
                    vidjeni.add(kljuc)
                    dogadaji_lista.append(dogadaj_podaci)
                
               
            
    return dogadaji_lista

@st.cache_data(ttl=86400)
def dohvati_opis_filma(url_filma):
    if not url_filma:
        return ""
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
    try:
        response=requests.get(url_filma,headers=headers,timeout=10)
        if response.status_code!=200:
            return ""
        soup=BeautifulSoup(response.text,"html.parser")
        multicol=soup.find("table",class_="wsite-multicol-table")
        if multicol:
            prvi_stupac=multicol.find("td",class_="wsite-multicol-col")
            if prvi_stupac:
                paragraf=prvi_stupac.find("div",class_="paragraph")
                if paragraf:
                    return paragraf.get_text(strip=True)
        return ""
    except Exception:
        return ""

@st.cache_data(ttl=3600)
def dohvati_filmove(url):
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
    try:
        response=requests.get(url,headers=headers,timeout=10)
    except requests.exceptions.RequestException:
        return []
    if response.status_code!=200:
        return []
    soup=BeautifulSoup(response.text,"html.parser")

    # Prikupljanje linkova filmova iz navigacijskog izbornika
    iskljuceni={"raspored","kontakt","index","pocetna","filmovi","arhiva",""}
    filmovi_linkovi={}
    for a in soup.find_all("a",href=True):
        href=a["href"].strip()
        tekst=a.get_text(strip=True).lower()
        if href.startswith("/") and href.endswith(".html"):
            ime=href.lstrip("/").rstrip(".html").split(".")[0]
            if ime not in iskljuceni and tekst:
                filmovi_linkovi[tekst]="https://www.kinogaj.hr"+href

    paragraf=soup.find("div",class_="paragraph")
    if paragraf is None:
        return []
    linije=paragraf.get_text(separator="\n").splitlines()
    linije=[l.replace("\xa0"," ").strip() for l in linije]
    linije=[l for l in linije if l and l!="\u200b"]

    def nadji_url(naslov):
        kljuc=naslov.lower().strip()
        if kljuc in filmovi_linkovi:
            return filmovi_linkovi[kljuc]
        for menu_naslov,url_filma in filmovi_linkovi.items():
            if kljuc in menu_naslov or menu_naslov.startswith(kljuc):
                return url_filma
        return None

    trenutni_datum=None
    zadnji_film=None
    zadnji_film_url=None
    filmovi=[]
    for linija in linije:
        if linija[0].isdigit():
            trenutni_datum=linija
        elif trenutni_datum and not linija.startswith("-") and linija not in ("#PROGRAM:","karta 5,00","EUR") and not linija.startswith("(") and not linija.startswith("u "):
            zadnji_film=linija
            zadnji_film_url=nadji_url(linija)
        elif trenutni_datum and linija.startswith("u "):
            filmovi.append({"datum":trenutni_datum,"naslov":zadnji_film,"vrijeme":linija,"url":zadnji_film_url})

    return filmovi

def _ics_escape(vrijednost):
    tekst = str(vrijednost or "")
    return (
        tekst.replace("\\", "\\\\")
        .replace(";", r"\;")
        .replace(",", r"\,")
        .replace("\r\n", r"\n")
        .replace("\r", r"\n")
        .replace("\n", r"\n")
    )


def generiraj_ics(dogadaj):
    datum_ics = datum_u_broj(dogadaj["datum"])
    pocetak = datetime.strptime(datum_ics, "%Y%m%d")
    kraj = pocetak + timedelta(days=1)
    dtstamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    uid = f"{uuid.uuid4()}@vz-gem"

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//vz_gem//Event Export//HR",
        "CALSCALE:GREGORIAN",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{dtstamp}",
        f"DTSTART;VALUE=DATE:{pocetak.strftime('%Y%m%d')}",
        f"DTEND;VALUE=DATE:{kraj.strftime('%Y%m%d')}",
        f"SUMMARY:{_ics_escape(dogadaj['naslov'])}",
        f"LOCATION:{_ics_escape(dogadaj['lokacija'])}",
        "END:VEVENT",
        "END:VCALENDAR",
        "",
    ]
    return "\r\n".join(lines)

def generiraj_ics_kino(film):
    datum_dt = datum_kino_u_datetime(film["datum"])
    if datum_dt is None:
        return ""
    kraj = datum_dt + timedelta(days=1)
    dtstamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    uid = f"{uuid.uuid4()}@vz-gem-kino"
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//vz_gem//Event Export//HR",
        "CALSCALE:GREGORIAN",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{dtstamp}",
        f"DTSTART;VALUE=DATE:{datum_dt.strftime('%Y%m%d')}",
        f"DTEND;VALUE=DATE:{kraj.strftime('%Y%m%d')}",
        f"SUMMARY:{_ics_escape(film['naslov'])}",
        "LOCATION:Kino Gaj",
        "END:VEVENT",
        "END:VCALENDAR",
        "",
    ]
    return "\r\n".join(lines)


def datum_u_datetime(datum_string):
    dijelovi = datum_string.split()
    if len(dijelovi) < 2:
        return None

    try:
        dan = int(dijelovi[0])
    except ValueError:
        return None

    kratica = dijelovi[1].lower()
    mjesec_broj = MJESECI.get(kratica, "01")
    try:
        mjesec = int(mjesec_broj)
    except ValueError:
        return None

    danas = datetime.now().date()
    kandidati = []
    for godina in (danas.year - 1, danas.year, danas.year + 1):
        try:
            kandidati.append(datetime(godina, mjesec, dan).date())
        except ValueError:
            continue

    if not kandidati:
        return None

    # Odabir prvog budućeg datuma, izbjegavanje prošlih datuma
    buduci=[dt for dt in kandidati if dt>=danas]
    if not buduci:
        return None
    odabrani = min(buduci, key=lambda dt: abs((dt - danas).days))
    return datetime.combine(odabrani, datetime.min.time())


def datum_u_broj(datum_string):
    datum = datum_u_datetime(datum_string)
    if datum is None:
        return "00000000"
    return datum.strftime("%Y%m%d")
def formatiraj_datum_kino(datum_string):
    dijelovi = datum_string.replace(" ", "").split(".")
    dan = dijelovi[0]
    mjesec_broj = dijelovi[1].zfill(2)
    mjesec_kratica = MJESECI_OBRNUTO.get(mjesec_broj, mjesec_broj)
    return f"{dan}.{mjesec_kratica}"

def datum_kino_u_datetime(datum_string):
    dijelovi = datum_string.strip().split(".")
    try:
        dan = int(dijelovi[0].strip())
        mjesec = int(dijelovi[1].strip())
    except (IndexError, ValueError):
        return None
    danas = datetime.now().date()
    try:
        return datetime(danas.year, mjesec, dan)
    except ValueError:
        return None

  
   
#strealit sučelje
st.set_page_config(page_title="Događaji u Varaždinu", page_icon="🎭",layout="centered")
odabrani_jezik=st.radio("Odaberite jezik/Select language: ",["Hrvatski HR","English EN"],horizontal=True)
postavke=JEZICI[odabrani_jezik]
st.markdown(f"""
    <div style="background-color:#4A0080; padding:20px; border-radius:10px; text-align:center;">
        <h1 style="color:white;">🎭 {postavke['naslov']}</h1>
        <p style="color:#E0C0FF;">{postavke['opis']}</p>
    </div>
""", unsafe_allow_html=True)


#gumb za dohvat kulturnih događaja
st.write("")
if st.button(postavke["gumb"]):
    with st.spinner("Dohvaćanje događaja..."):#vizualizacija pretrage
        rezultati=dohvati_dogadaje(postavke["url"])
        danas = datetime.now().date()
        filtrirani_rezultati = []
        for d in rezultati:
            datum_eventa = datum_u_datetime(d["datum"])
            if datum_eventa and datum_eventa.date() >= danas:
                filtrirani_rezultati.append(d)
        rezultati = sorted(filtrirani_rezultati, key=lambda d: datum_u_broj(d["datum"]))
    if rezultati:
        st.success(postavke["Uspjeh"].format(len(rezultati))) #ispis rezultata na web stranicu
        st.caption(f"🕐 {postavke['dohvaceno']} {datetime.now(ZoneInfo('Europe/Zagreb')).strftime('%H:%M')}")
        for i, d in enumerate(rezultati):
            with st.expander(f"🎭 {d['naslov']}"):

                
                st.markdown(f"📅 **{postavke['lbl_datum']}:** {d['datum']} | ⏰ **{postavke['lbl_vrijeme']}:** {d['vrijeme']}")
                st.caption(f"📍 **{postavke['lbl_lokacija']}:** {d['lokacija']}")   
                         
                ics_data=generiraj_ics(d)
                st.download_button(
                    label="📅 Dodaj u kalendar",
                    data=ics_data,
                    file_name=f"{d['naslov']}.ics",
                    mime="text/calendar",
                    key=f"download_ics_{i}"
                )         
                st.divider() 
    else:
        st.error(postavke["greska"])

#gumb za prihvat kino događaja
st.write("")
if st.button( postavke['gumb_kino']):
    with st.spinner(postavke["ucitavanje_kino"]):
        filmovi=dohvati_filmove(URL_KINO_GAJ)
        danas=datetime.now().date()
        
        filmovi=[f for f in filmovi if (dt:=datum_kino_u_datetime(f["datum"])) and dt.date()>=danas]
        
    if filmovi:
        st.success(postavke["uspjeh_kino"].format(len(filmovi)))
        for i,f in enumerate(filmovi):
            with st.expander(f"🎬 {f['naslov']}"):
                st.markdown(f"📅 **{postavke['lbl_datum']}:** {formatiraj_datum_kino(f['datum'])} | ⏰ **{postavke['lbl_vrijeme']}:** {f['vrijeme']}")
                opis=dohvati_opis_filma(f.get("url"))
                if opis:
                    st.markdown(f"_{opis}_")

                ics_data=generiraj_ics_kino(f)
                if ics_data:
                    st.download_button(
                    label="📅 Dodaj u kalendar",
                    data=ics_data,
                    file_name=f"{f['naslov']}.ics",
                    mime="text/calendar",
                    key=f"download_ics_{i}"
                )
                st.divider()
            
    else:
        st.error(postavke["greska_kino"])


st.markdown(
    "<p style='text-align:center; margin-top:80px; color:gray;'>"
    "Powered by Filip (20% Digital)</p>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div style='text-align:center; margin-top:10px;'>"
    "<a href='https://paypal.me/filipvz' target='_blank'>"
    "<button style='background-color:#0070ba; color:white; border:none; "
    "padding:10px 24px; border-radius:6px; cursor:pointer; font-size:15px;'>"
    "💙 Podržite projekt</button></a></div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center; margin-top:80px; color:gray;'>"
    "Version 1.0</p>",
    unsafe_allow_html=True,
)
        




