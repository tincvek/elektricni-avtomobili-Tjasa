import re
import os
import json
import html
from konstante import ZNAMKE_IN_DRZAVE

vzorec = re.compile(
    r'<a\s+href="(?P<link>https://bestev4me.eu/ev-catalog/[^"]+)"[^>]*>\s*'
    r'<h4[^>]*>(?P<znamka>.*?)</h4>\s*'
    r'<h3[^>]*>(?P<model>.*?)</h3>',
    re.DOTALL
)

def osnovni_podatki(stevilo_strani):
    osnovni = []
    
    for i in range(1, stevilo_strani + 1):
        pot_datoteke = f"podatki/html_strani/stran{i}.html"
        print(f"Preverjam pot: {os.path.abspath(pot_datoteke)}")
        if not os.path.exists(pot_datoteke):
            print(f"html{i}-te strani nism našel")
            continue
            
        with open(pot_datoteke, "r", encoding="utf-8") as dat:
            vsebina = dat.read()

        for najdba in vzorec.finditer(vsebina):
            info = {
                "znamka": najdba["znamka"].strip(),
                "model": najdba["model"].strip(),
                "link": najdba["link"],
            }
            osnovni.append(info)
            
    # odstrani duplikate po linku
    videni_linki = set()
    unikatni_osnovni = []
    for avto in osnovni:
        if avto["link"] not in videni_linki:
            videni_linki.add(avto["link"])
            unikatni_osnovni.append(avto)

    with open("podatki/vsi_avtomobili.json", "w", encoding="utf-8") as f:
        json.dump(unikatni_osnovni, f, ensure_ascii=False, indent=4)
    print(f"Shranjenih {len(unikatni_osnovni)} avtomobilov v vsi_avtomobili.json")

    return unikatni_osnovni

def podrobnosti_modelov(podatki_in_htmlji):
    modeli = []
    for podatki_modela, html_modela in podatki_in_htmlji:
        podrobnosti = izlusci_podrobnosti_o_modelu(html_modela, podatki_modela["znamka"])
        modeli.append(podrobnosti | podatki_modela)
    
    return modeli

def izlusci_podrobnosti_o_modelu(html_modela, znamka):
    doseg_re = re.search(r'Range.*?<div[^>]*>([\d\.]+)\s*km</div>', html_modela, re.DOTALL)
    poraba_re = re.search(r'Efficiency.*?<div[^>]*>([\d\.]+)\s*kWh/100km</div>', html_modela, re.DOTALL | re.IGNORECASE)
    baterija_re = re.search(r'Battery size.*?<div[^>]*>([\d\.]+)\s*kWh</div>', html_modela, re.DOTALL | re.IGNORECASE)
    polnjenje_re = re.search(r'Charging.*?<div[^>]*>(\d+)\s*min/100\s*km</div>', html_modela, re.DOTALL)
    pospesek_re = re.search(r'Acceleration.*?<div[^>]*>([\d\.]+)\s*sec</div>', html_modela, re.DOTALL)
    cena_re = re.search(r'Price \(DE\).*?<div>\s*([\d\x27\s]+)\s*EUR\s*</div>', html_modela, re.DOTALL)

    return {
        "doseg_[km]": float(doseg_re.group(1)) if doseg_re else None,
        "poraba_[kWh/100km]": float(poraba_re.group(1)) if poraba_re else None,
        "kapaciteta_[kWh]": float(baterija_re.group(1)) if baterija_re else None,
        "cas_polnjenja(10-80%)_[min]": int(polnjenje_re.group(1)) if polnjenje_re else None,
        "pospesek(0-100km/h)_[s]": float(pospesek_re.group(1)) if pospesek_re else None,
        "cena_[EUR]": int(cena_re.group(1).replace('\x27', '').strip()) if cena_re else None,
        "drzava": ZNAMKE_IN_DRZAVE.get(znamka, "Neznano")
    }
    



