from fastapi import FastAPI
from db import insert_supplements_from_csv
from api import setup_routes
import uvicorn
import argparse
# from pull_data import build_dsld_uses_json

app = FastAPI()
setup_routes(app)

if __name__ == "__main__":
    print   ("Starting NutriAI server...")
    parser = argparse.ArgumentParser(description="NutriAI server / DB setup")
    parser.add_argument("--load-data", action="store_true", help="Load supplements CSV into the database")
    parser.add_argument("--get-url-data", action="store_true", help="Download and extract all Health Canada data")

    args = parser.parse_args()

    if args.get_url_data:
        from url import download_all
        print("Downloading and extracting Health Canada data...")
        download_all()
    if args.load_data:
        print("Loading supplements data into the database...")
        insert_supplements_from_csv()

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
