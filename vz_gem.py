import streamlit as st  
import requests
from bs4 import BeautifulSoup

JEZICI={
    "Hrvatski HR":{
        "url":"https://www.tourism-varazdin.hr/kalendar-dogadanja/",
        "naslov":"Događaji u varaždinu",
        "opis":"Dobrodošli u našu aplikaciju koja prikazuje događaje u Varaždinu",
        "gumb":"Dohvati najnovije događaje",
        "ucitavanje":"Dohvaćanje događaja...",
        "Uspjeh":"Pronađeno je {} događaja.",
        "greska":"Nema dostupnih događaja.",
        "lbl_datum":"Datum",
        "lbl_vrijeme":"Vrijeme",
        "lbl_lokacija":"Lokacija",
        "lbl_naslov":"Naslov"
        
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
        "lbl_naslov":"Title"
        
    }
}

def dohvati_dogadaje(postavke_jezika):
    URL=postavke_jezika["url"]
    headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    
    response=requests.get(URL,headers=headers)#GET zahtjer za server
    dogadaji_lista=[]
    if response.status_code==200: #status kod 200 ok provjera servera
        
        soup=BeautifulSoup(response.text,"html.parser")
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

                
                dogadaji_lista.append(dogadaj_podaci)
            
    return dogadaji_lista

#strealit sučelje
st.set_page_config(page_title="Događaji u Varaždinu", page_icon="🎭",layout="centered")
odabrani_jezik=st.radio("odaberite jezik/Select language: ",["Hrvatski HR","English EN"],horizontal=True)
postavke=JEZICI[odabrani_jezik]

st.title(postavke["naslov"])
st.write(postavke["opis"])

#gumb za dohvat događaja
if st.button(postavke["gumb"]):
    with st.spinner("Dohvaćanje događaja..."):#vizualizacija pretrage
        rezultati=dohvati_dogadaje(postavke)
    if rezultati:
        st.success(postavke["Uspjeh"].format(len(rezultati))) #ispis rezultata na web stranicu
        for d in rezultati:
            with st.container():
                st.subheader(d['naslov'])
                st.markdown(f"📅 **{postavke['lbl_datum']}:** {d['datum']} | ⏰ **{postavke['lbl_vrijeme']}:** {d['vrijeme']}")
                st.caption(f"📍 **{postavke['lbl_lokacija']}:** {d['lokacija']}")
                st.divider()                 
                
    else:
        st.error(postavke["greska"])
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

st.write("Powered by Filip (20% Digital)")  
        



