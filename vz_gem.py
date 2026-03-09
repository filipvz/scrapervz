import streamlit as st  
import requests
from bs4 import BeautifulSoup
import uuid
from datetime import datetime,timedelta


MJESECI={
    "sij":"01","vel":"02","ožu":"03",
    "tra":"04","svi":"05","lip":"06",
    "srp":"07","kol":"08","ruj":"09",
    "lis":"10","stu":"11","pro":"12"
}
JEZICI={
    "Hrvatski HR":{
        "url":"https://www.tourism-varazdin.hr/kalendar-dogadanja/",
        "naslov":"Događaji u Varaždinu",
        "opis":"Dobrodošli u našu aplikaciju koja prikazuje događaje u Varaždinu",
        "gumb":"Dohvati najnovije događaje",
        "ucitavanje":"Dohvaćanje događaja...",
        "Uspjeh":"Pronađeno je {} događaja.",
        "greska":"Nema dostupnih događaja.",
        "lbl_datum":"Datum",
        "lbl_vrijeme":"Vrijeme",
        "lbl_lokacija":"Lokacija",
        "lbl_naslov":"Naslov",
        "dohvaceno":"Podaci dohvaćeni u "
        
    },
    "English EN":{
        "url":"https://www.tourism-varazdin.hr/kalendar-dogadanja/",
        "naslov":"Events in Varaždin",
        "opis":"Welcome to our application that displays events in Varaždin",
        "gumb":"Get latest events",
        "ucitavanje":"Loading events...",
        "Uspjeh":"Found {} events.",
        "greska":"No events available.",
        "lbl_datum":"Date",
        "lbl_vrijeme":"Time",
        "lbl_lokacija":"Location",
        "lbl_naslov":"Title",
        "dohvaceno":"Events loaded at "
        
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

def _ics_escape(vrijednost):
    tekst = str(vrijednost or "")
    return (
        tekst.replace("\\", "\\\\")
        .replace(";", r"\;")
        .replace(",", r"\,")
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


#gumb za dohvat događaja
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
        st.caption(f"🕐 {postavke['dohvaceno']} {datetime.now().strftime('%H:%M')}")
        for i, d in enumerate(rezultati):
            with st.expander(d['naslov']):
                
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
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

st.write("Powered by Filip (20% Digital)")  
        



