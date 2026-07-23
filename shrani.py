import csv
import os

def zapisi_csv(fieldnames, rows, directory, filename):
    """Zapise podatke iz 'rows' v CSV datoteko 'directory'/'filename',
    z stolpci definiranimi v 'fieldnames'."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def zapisi_modele_csv(modeli, directory, filename):
    """Zapise podatke o modelih v CSV datoteko. Predpostavi, da imajo vsi
    slovarji v 'modeli' enake kljuce in da seznam ni prazen."""
    assert modeli and all(m.keys() == modeli[0].keys() for m in modeli)
    zapisi_csv(modeli[0].keys(), modeli, directory, filename)
