from bs4 import BeautifulSoup
import requests
import pandas as pd

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/103.0.0.0 Safari/537.36',
    'accept-language': "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-ch-ua-platform": "Windows",
    "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"'
}
nama_barang = []
harga_barang = []
link_barang = []


def list_harga(page):
    url = f"https://www.tokopedia.com/search?page={page}&q=ram%208gb%20ddr4%203200mhz%20sodimm&" \
          f"source=universe&srp_component_id=02.07.01.01&st=product"

    page = requests.Session().get(url, headers=headers).text
    # print(page)
    doc = BeautifulSoup(page, "html.parser")
    page_text = doc.find_all(class_="css-974ipl")
    if len(page_text) > 0:
        for i in page_text:
            name = i.find_next(class_="css-1b6t4dn").string
            harga = i.find_next(class_='css-1ksb19c').string
            link = i.find_next(class_="pcv3__info-content css-gwkf0u")['href']
            nama_barang.append(name)
            harga_barang.append(harga)
            link_barang.append(link)
            return True
    else:
        print("Berhenti")
        df = pd.DataFrame([nama_barang, harga_barang, link_barang])
        df.to_excel("ram.xlsx", index=False)
        return False


halaman = 1

hasil = True
while hasil:
    out_put = list_harga(halaman)
    halaman += 1
    if not out_put:
        hasil = False
