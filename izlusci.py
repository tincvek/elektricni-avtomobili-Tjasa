import re
import os
import json
from konstante import ZNAMKE_IN_DRZAVE

vzorec = re.compile(
    r'<a\s+href="(?P<link>https://bestev4me.eu/ev-catalog/[^"]+)"[^>]*>\s*'
    r'<h4[^>]*>(?P<znamka>.*?)</h4>\s*'
    r'<h3[^>]*>(?P<model>.*?)</h3>',
    re.DOTALL
)

def odstrani_duplikate(seznam, kljuc):
    """Odstrani podvojene elemente iz seznama slovarjev glede na dani ključ,
    pri čemer obdrži prvo pojavitev vsakega unikatnega vnosa."""
    videni = set()
    unikatni = []
    for element in seznam:
        if element[kljuc] not in videni:
            videni.add(element[kljuc])
            unikatni.append(element)
    return unikatni

def osnovni_podatki(stevilo_strani):
    """Na vsaki strani izlušči osnovne podatke (znamka, model, link) vseh avtomobilov,
    odstrani morebitne duplikate avtomobilov in jih zaradi preglednosti shrani v json datoteko."""
    osnovni = []

    for i in range(1, stevilo_strani + 1):
        pot_datoteke = f"podatki/html_strani/stran{i}.html"

        if not os.path.exists(pot_datoteke):
            print(f"html{i}-te strani nisem našel")
            continue

        with open(pot_datoteke, "r", encoding="utf-8") as dat:
            vsebina = dat.read()

        for najdba in vzorec.finditer(vsebina):
            osnovni.append({
                "znamka": najdba["znamka"].strip(),
                "model": najdba["model"].strip(),
                "link": najdba["link"],
            })

    unikatni_osnovni = odstrani_duplikate(osnovni, "link")

    with open("podatki/vsi_avtomobili.json", "w", encoding="utf-8") as f:
        json.dump(unikatni_osnovni, f, ensure_ascii=False, indent=4)

    print(f"Shranjenih {len(unikatni_osnovni)} avtomobilov v vsi_avtomobili.json")
    return unikatni_osnovni

def podrobnosti_modelov(podatki_in_htmlji):
    """Sprejme seznam parov (slovar, string) in iz stringa izlusci slovar podrobnosti
    ter ga združi s slovarjem osnovnih podatkov."""
    modeli = []
    for podatki_modela, html_modela in podatki_in_htmlji:
        podrobnosti = izlusci_podrobnosti_o_modelu(html_modela, podatki_modela["znamka"])
        modeli.append(podrobnosti | podatki_modela)
    
    return modeli

def izlusci_podrobnosti_o_modelu(html_modela, znamka):
    """"Naredi slovar podrobnosti vsakega modela."""
    doseg_re = re.search(r'Range.*?<div[^>]*>([\d\.]+)\s*km</div>', html_modela, re.DOTALL)
    poraba_re = re.search(r'Efficiency.*?<div[^>]*>([\d\.]+)\s*kWh/100km</div>', html_modela, re.DOTALL | re.IGNORECASE)
    baterija_re = re.search(r'Battery size.*?<div[^>]*>([\d\.]+)\s*kWh</div>', html_modela, re.DOTALL | re.IGNORECASE)
    polnjenje_re = re.search(r'Charging.*?<div[^>]*>(\d+)\s*min/100\s*km</div>', html_modela, re.DOTALL)
    pospesek_re = re.search(r'Acceleration.*?<div[^>]*>([\d\.]+)\s*sec</div>', html_modela, re.DOTALL)
    cena_re = re.search(r'Price\s+(.+?)\s*EUR', html_modela)
    leto_re = re.search(r'Available since\s+\d{2}-(\d{4})', html_modela, re.DOTALL)


    return {
    "doseg_[km]": float(doseg_re.group(1)) if doseg_re else None,
    "poraba_[kWh/100km]": float(poraba_re.group(1)) if poraba_re else None,
    "kapaciteta_[kWh]": float(baterija_re.group(1)) if baterija_re else None,
    "cas_polnjenja[min/100km]": int(polnjenje_re.group(1)) if polnjenje_re else None,
    "pospesek(0-100km/h)_[s]": float(pospesek_re.group(1)) if pospesek_re else None,
    "cena_[EUR]": int(re.sub(r'\D', '', cena_re.group(1))) if cena_re else None,
    "drzava": ZNAMKE_IN_DRZAVE.get(znamka, "Neznano"),
    "leto": int(leto_re.group(1)) if leto_re else None
}

