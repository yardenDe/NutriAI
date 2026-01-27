import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin, urlparse
import os
import zipfile    
from file_parser import merge_products_purposes

BASE_URL = "https://www.canada.ca"
PAGE_URL = "https://www.canada.ca/en/health-canada/services/drugs-health-products/natural-non-prescription/applications-submissions/product-licensing/licensed-natural-health-product-database-data-extract.html"
STEM = [
    "NHP_PRODUCTS_PURPOSE",
    "NHP_PRODUCTS",
    "NHP_MEDICINAL_INGREDIENTS",
    "NHP_NONMEDICINAL_INGREDIENTS"
]
EXT = ".zip"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "DataBase"



def find_links_generator(soup):
    links = soup.find_all("a", href=True)
    for link in links:
        href = link["href"]
        if any(s+EXT in href for s in STEM):
            full_url = urljoin(BASE_URL, href)
            yield full_url

def download_file(full_url: str, output_dir: str) -> str:
    filename = Path(urlparse(full_url).path).name
    output_file = os.path.join(output_dir, filename)

    response = requests.get(full_url)
    response.raise_for_status()

    with open(output_file, "wb") as f:
        f.write(response.content)

    print(f" Saved: {output_file}")
    return output_file

def download_all():
    response = requests.get(PAGE_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for full_link in find_links_generator(soup):
        output_file = download_file(full_link, OUTPUT_DIR)

        with zipfile.ZipFile(output_file, 'r') as zip_ref:
            zip_ref.extractall(OUTPUT_DIR)   
        
        os.remove(output_file)

    merge_products_purposes()


