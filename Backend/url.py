import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

BASE_URL = "https://www.canada.ca"
PAGE_URL = "https://www.canada.ca/en/health-canada/services/drugs-health-products/natural-non-prescription/applications-submissions/product-licensing/licensed-natural-health-product-database-data-extract.html"
STEM = [
    "NHP_PRODUCTS_PURPOSE",
    "NHP_PRODUCTS",
    "NHP_MEDICINAL_INGREDIENTS",
    "NHP_NONMEDICINAL_INGREDIENTS"
]
EXT = ".zip"
OUTPUT_DIR = "sup_data"

def create_path(OUTPUT_DIR):
    path = os.path.join(os.getcwd(), OUTPUT_DIR)
    os.makedirs(path, exist_ok=True)
    return path

def get_filename_from_url(file_url):
    parts = file_url.split("/")
    return parts[-1]

def find_links_generator(soup):
    links = soup.find_all("a", href=True)
    for link in links:
        href = link["href"]
        if any(s+EXT in href for s in STEM):
            full_url = urljoin(BASE_URL, href)
            yield full_url

def download_file(file_url, output_dir):
    pass

if __name__ == "__main__":
        
    response = requests.get(PAGE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    for full_link in find_links_generator(soup):
        print(full_link)

    create_path(OUTPUT_DIR)
    
