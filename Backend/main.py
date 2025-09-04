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
    parser.add_argument("--load-csv", action="store_true", help="Load supplements CSV into the database")
    args = parser.parse_args()

    if args.load_csv:
        insert_supplements_from_csv()
        print("CSV data inserted into DB.")

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
