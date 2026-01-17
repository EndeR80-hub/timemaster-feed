import requests
from lxml import etree

def process_xml():
    url = "https://www.dobrezegarki.pl/google-merchant_id-1.xml"
    ns = {"g": "http://base.google.com/ns/1.0"}
    
    # Dane GPSR - PH Hermes Sp. z o.o.
    RESP_NAME = "PH Hermes Sp. z o.o."
    RESP_ADDR = "ul. Leopolda 31, 40-189 Katowice, Polska"
    RESP_EMAIL = "timemaster@phhermes.pl"
    RESP_PHONE = "609473793"

    print("Pobieranie i przetwarzanie danych...")
    response = requests.get(url)
    if response.status_code != 200:
        return

    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.fromstring(response.content, parser)

    for item in root.xpath(".//item"):
        # 1. MPN / MODEL / KOD_PRODUCENTA
        mpn_el = item.find("g:mpn", namespaces=ns)
        if mpn_el is not None and mpn_el.text:
            symbol = mpn_el.text
            index = item.index(mpn_el)
            
            for tag, offset in [("model", 1), ("kod_producenta", 2)]:
                old_el = item.find(f"g:{tag}", namespaces=ns)
                if old_el is not None: item.remove(old_el)
                new_el = etree.Element(f"{{{ns['g']}}}{tag}")
                new_el.text = symbol
                item.insert(index + offset, new_el)

        # 2. DODAWANIE DANYCH GPSR (Standard Google Merchant)
        gpsr_data = [
            ("responsible_person_name", RESP_NAME),
            ("responsible_person_address", RESP_ADDR),
            ("responsible_person_email", RESP_EMAIL),
            ("responsible_person_phone", RESP_PHONE)
        ]

        for tag_name, value in gpsr_data:
            # Usuwamy stare, by nie dublować
            old_tag = item.find(f"g:{tag_name}", namespaces=ns)
            if old_tag is not None: item.remove(old_tag)
            
            # Wstawiamy nowe tagi g:
            new_tag = etree.SubElement(item, f"{{{ns['g']}}}{tag_name}")
            new_tag.text = value

    # Zapis do pliku
    tree = etree.ElementTree(root)
    tree.write("output.xml", encoding="utf-8", xml_declaration=True, pretty_print=True)
    print("Sukces! Plik z danymi GPSR gotowy.")

if __name__ == "__main__":
    process_xml()
