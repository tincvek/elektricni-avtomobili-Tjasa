# Analiza električnih avtomobilov
## Uvod

Za projektno nalogo pri predmetu Uvod v programiranje sem podatke črpala iz spletne strani bestev4me.eu, kjer je zbran katalog električnih avtomobilov. Za vsak avtomobil so na voljo podatki o znamki, modelu, letu izdaje, dosegu, porabi, kapaciteti baterije, času polnjenja, pospešku (0–100 km/h) in ceni. Poleg tega sem vsaki znamki avtomobila glede na podatke iz konstante ZNAMKE_IN_DRZAVE pripisala tudi državo izvora.

Na dan pridobivanja podatkov je bilo v katalogu zajetih 67 strani z avtomobili, kar znaša okoli 1300 unikatnih modelov.

## Navodila za uporabo

Glavna datoteka, s katero lahko uporabnik zažene program, je main.py. Ta po vrsti pokliče pridobivanje HTML strani (pridobi.py), izluščevanje podatkov iz njih (izlusci.py) in zapis podatkov v CSV datoteko (shrani.py). Program potrebuje knjižnico requests (pip install requests).

Ker sem HTML strani in podstrani modelov med razvojem že prenesla in jih uporabljala kot predpomnilnik, je v main.py vrstica za njihov ponoven zajem privzeto zakomentirana.

Če želite podatke zajeti na novo (npr. za posodobitev kataloga), to vrstico odkomentirajte in poženite main.py. Ker gre za zamuden postopek (prenos ~1300 spletnih strani), ga sicer pustite zakomentiranega – priloženi so že izluščeni podatki v podatki/vsi_avtomobili.json in podatki/avtomobili.csv.

Za analizo podatkov poženite analiza.ipynb, ki podatke prebere iz podatki/avtomobili.csv in potrebuje knjižnici pandas in matplotlib.

## Analiza podatkov

Datoteka analiza.ipynb pripravi tabelarično in grafično analizo pridobljenih podatkov – med drugim primerja cene, doseg, kapaciteto baterije in čas polnjenja med znamkami, državami in letniki vozil ter poišče osamelce v podatkih.

