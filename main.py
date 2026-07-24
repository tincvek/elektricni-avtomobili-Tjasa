import pridobi
import izlusci
import shrani


STEVILO_STRANI = 67

# pridobi.pridobi_htmlje(STEVILO_STRANI)

osnovni_podatki = izlusci.osnovni_podatki(STEVILO_STRANI)
print(f"Št. osnovnih podatkov: {len(osnovni_podatki)}") 

podatki_in_htmlji = pridobi.pridobi_htmlje_avtomobilov(osnovni_podatki)
print(f"Št. prenesenih HTML-jev: {len(podatki_in_htmlji)}") 

avtomobili = izlusci.podrobnosti_modelov(podatki_in_htmlji)
print(f"Št. izluščenih avtomobilov: {len(avtomobili)}")  

shrani.zapisi_modele_csv(avtomobili, "podatki", "avtomobili_csv")


