from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from url import download_all

from chat_router import router as chat_router
from user_router import router as user_router
from supp_router import router as supp_router

import uvicorn
import argparse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(user_router)
app.include_router(supp_router)


if __name__ == "__main__":
    print   ("Starting NutriAI server...")
    parser = argparse.ArgumentParser(description="NutriAI server / DB setup")
    parser.add_argument("--load-data", action="store_true", help="Load supplements CSV into the database")
    parser.add_argument("--get-url-data", action="store_true", help="Download and extract all Health Canada data")

    args = parser.parse_args()

    if args.get_url_data:
        print("Downloading and extracting Health Canada data...")
        download_all()
    if args.load_data:
        print("Loading supplements data into the database...")
        # insert_supplements_from_csv()

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
