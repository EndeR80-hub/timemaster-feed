import requests
from lxml import etree

def process_xml():
    url = "https://www.dobrezegarki.pl/google-merchant_id-1.xml"
    ns = {"g": "http://base.google.com/ns/1.0"}

    response = requests.get(url)
    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.fromstring(response.content, parser)

    for item in root.xpath(".//item"):
        mpn_el = item.find("g:mpn", namespaces=ns)
        if mpn_el is not None and mpn_el.text:
            symbol = mpn_el.text
            for tag in ["model", "kod_producenta"]:
                tag_path = f"{{{ns['g']}}}{tag}"
                element = item.find(f"g:{tag}", namespaces=ns)
                if element is None:
                    element = etree.SubElement(item, tag_path)
                element.text = symbol

    tree = etree.ElementTree(root)
    tree.write("output.xml", encoding="utf-8", xml_declaration=True, pretty_print=True)

if __name__ == "__main__":
    process_xml()
