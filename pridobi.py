import os
import requests
import time

HEADERS = {"User-Agent": "Mozilla/5.0"}

def pridobi_htmlje(stevilo_strani, mapa= "podatki/html_strani"):
    
    os.makedirs(mapa, exist_ok=True)
    for i in range(1, stevilo_strani + 1):
        pot_datoteke = os.path.join(mapa, f"stran{i}.html")

        if os.path.exists(pot_datoteke):
            print(f"html_stran{i} že obstaja, preskočim")
            continue

        odgovor = requests.get(
            f"https://bestev4me.eu/ev-catalog?page={i}",
            headers=HEADERS,
        )
        if odgovor.status_code != 200:
            print(f"napaka pri prenosu {i}-te strani")
            continue

        vsebina = odgovor.text

        with open(pot_datoteke, "w", encoding="utf-8") as dat:
            dat.write(vsebina)
            print(f"html_stran{i} shranjena")

        time.sleep(1)

def pridobi_htmlje_avtomobilov(osnovni_podatki, mapa="podatki/html_modeli"):
    """Prenese in shrani HTML strani posameznih modelov avtomobilov 
        ter naredi seznam parov (podatki_modela, html_modela)."""
    os.makedirs(mapa, exist_ok=True)
    podatki_in_htmlji = []

    for podatek in osnovni_podatki:
        url = podatek["link"]
        ime_datoteke = f"model_{url.strip('/').split('/')[-1]}.html"
        pot_datoteke = os.path.join(mapa, ime_datoteke)

        # if os.path.exists(pot_datoteke):
        print(f"{ime_datoteke} ze prenesena, preskočim")
        with open(pot_datoteke, "r", encoding="utf-8") as f:
                podatki_in_htmlji.append((podatek,f.read()))
        #     continue

        # odgovor = requests.get(url, headers=HEADERS)
        
        # if odgovor.status_code != 200:
        #     print(f"Napaka pri prenosu: {odgovor.status_code} - {url}")
        #     continue

        # vsebina = odgovor.text
        # with open(pot_datoteke, "w", encoding="utf-8") as f:
        #     f.write(vsebina)

        # podatki_in_htmlji.append((podatek, vsebina))
        # print(f"Prenesen model: {podatek['znamka']} {podatek['model']}")

        # time.sleep(1)

    return podatki_in_htmlji