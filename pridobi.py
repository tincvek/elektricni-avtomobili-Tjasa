import os
import requests
import time

HEADERS = {"User-Agent": "Mozilla/5.0"}

def pridobi_ali_preberi_html(url, pot_datoteke):
    """Vrne HTML vsebino strani - iz lokalne datoteke, če že obstaja,
    sicer jo prenese s spleta in shrani."""
    if os.path.exists(pot_datoteke):
        with open(pot_datoteke, "r", encoding="utf-8") as f:
            return f.read()

    odgovor = requests.get(url, headers=HEADERS)
    if odgovor.status_code != 200:
        print(f"Napaka pri prenosu: {odgovor.status_code} - {url}")
        return None

    vsebina = odgovor.text
    with open(pot_datoteke, "w", encoding="utf-8") as f:
        f.write(vsebina)

    time.sleep(1) 
    return vsebina

def pridobi_htmlje(stevilo_strani, mapa="podatki/html_strani"):
    """Shrani s splelta ali prebere ze shranjeno HTML-datoteko za vsako stran."""
    os.makedirs(mapa, exist_ok=True)
    for i in range(1, stevilo_strani + 1):
        pot_datoteke = os.path.join(mapa, f"stran{i}.html")
        url = f"https://bestev4me.eu/ev-catalog?page={i}"
        pridobi_ali_preberi_html(url, pot_datoteke)


def pridobi_htmlje_avtomobilov(osnovni_podatki, mapa="podatki/html_modeli"):
    """Prenese in shrani HTML strani posameznih modelov avtomobilov ter
      naredi seznam parov (osnovni_podatki_modela(slovar), html_modela(string))."""
    os.makedirs(mapa, exist_ok=True)
    podatki_in_htmlji = []

    for podatek in osnovni_podatki:
        url = podatek["link"]
        ime_datoteke = f"model_{url.strip('/').split('/')[-1]}.html"
        pot_datoteke = os.path.join(mapa, ime_datoteke)

        vsebina = pridobi_ali_preberi_html(url, pot_datoteke)
        if vsebina is not None:
            podatki_in_htmlji.append((podatek, vsebina))

    return podatki_in_htmlji