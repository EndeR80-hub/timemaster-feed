import requests
from lxml import etree

def process_xml():
    url = "https://www.dobrezegarki.pl/google-merchant_id-1.xml"
    ns = {"g": "http://base.google.com/ns/1.0"}
    
    print("Pobieranie pliku...")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Błąd pobierania: {response.status_code}")
        return

    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.fromstring(response.content, parser)

    items = root.xpath(".//item")
    for item in items:
        # 1. Znajdź element mpn
        mpn_el = item.find("g:mpn", namespaces=ns)
        
        if mpn_el is not None and mpn_el.text:
            symbol = mpn_el.text
            
            # Pobieramy indeks (pozycję) elementu mpn
            index = item.index(mpn_el)
            
            # 2. Usuwamy stare tagi model/kod_producenta jeśli istnieją, 
            # aby uniknąć dublowania przy ponownym uruchomieniu
            for tag in ["model", "kod_producenta"]:
                old_el = item.find(f"g:{tag}", namespaces=ns)
                if old_el is not None:
                    item.remove(old_el)
            
            # 3. Wstawiamy nowe tagi zaraz po mpn (index + 1, index + 2)
            # Tworzymy elementy ręcznie, aby móc kontrolować ich pozycję
            
            model_el = etree.Element(f"{{{ns['g']}}}model")
            model_el.text = symbol
            item.insert(index + 1, model_el)
            
            kod_el = etree.Element(f"{{{ns['g']}}}kod_producenta")
            kod_el.text = symbol
            item.insert(index + 2, kod_el)

    # Zapis do pliku
    tree = etree.ElementTree(root)
    tree.write("output.xml", encoding="utf-8", xml_declaration=True, pretty_print=True)
    print("Sukces! Tagi wstawione po MPN.")

if __name__ == "__main__":
    process_xml()
