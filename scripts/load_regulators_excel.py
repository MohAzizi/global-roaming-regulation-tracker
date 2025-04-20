import pandas as pd, re, pathlib
from pymongo import MongoClient


BASE_DIR = pathlib.Path(__file__).resolve().parents[1]   # …/global-roaming-regulation-tracker
EXCEL = BASE_DIR / "data" / "Telecom_Regulatory_Authorities_Global.xlsx"
MONGO_URI = "mongodb://localhost:27017"        # or Atlas URI
DB_NAME = "roaming_tracker"
COLL_NAME = "regulators_raw"

def snake(name:str)->str:
    """Convert column names to snake_case."""
    return re.sub(r'\W+', '_', name).strip('_').lower()

def main():
    df = pd.read_excel(EXCEL)
    df.columns = [snake(c) for c in df.columns]

    client = MongoClient(MONGO_URI)
    coll = client[DB_NAME][COLL_NAME]
    coll.delete_many({})          # idempotent reload while prototyping
    coll.insert_many(df.to_dict("records"))
    print(f"Loaded {coll.count_documents({})} rows into {DB_NAME}.{COLL_NAME}")

if __name__ == "__main__":
    main()
