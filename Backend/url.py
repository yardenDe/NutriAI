import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import zipfile        

BASE_URL = "https://www.canada.ca"
PAGE_URL = "https://www.canada.ca/en/health-canada/services/drugs-health-products/natural-non-prescription/applications-submissions/product-licensing/licensed-natural-health-product-database-data-extract.html"
STEM = [
    "NHP_PRODUCTS_PURPOSE",
    "NHP_PRODUCTS",
    "NHP_MEDICINAL_INGREDIENTS",
    "NHP_NONMEDICINAL_INGREDIENTS"
]
EXT = ".zip"
OUTPUT_DIR_NAME = "sup_data"

def create_path(dir_name: str) -> str:
    path = os.path.join(os.getcwd(), dir_name)
    os.makedirs(path, exist_ok=True)
    return path

def get_filename_from_url(file_url: str) -> str:
    return os.path.basename(urlparse(file_url).path)
    

def find_links_generator(soup):
    links = soup.find_all("a", href=True)
    for link in links:
        href = link["href"]
        if any(s+EXT in href for s in STEM):
            full_url = urljoin(BASE_URL, href)
            yield full_url

def download_file(full_url: str, output_dir: str) -> str:
    filename = get_filename_from_url(full_url)
    output_file = os.path.join(output_dir, filename)

    response = requests.get(full_url)
    response.raise_for_status()

    with open(output_file, "wb") as f:
        f.write(response.content)

    print(f" Saved: {output_file}")
    return output_file


if __name__ == "__main__":
    output_dir = create_path(OUTPUT_DIR_NAME)

    response = requests.get(PAGE_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for full_link in find_links_generator(soup):
        OUTPUT_FILE = download_file(full_link, output_dir)

        with zipfile.ZipFile(OUTPUT_FILE, 'r') as zip_ref:
            zip_ref.extractall(output_dir)   
        
        os.remove(OUTPUT_FILE)  # Optionally remove the zip file after extraction


