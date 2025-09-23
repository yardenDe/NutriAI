from pathlib import Path
import pandas as pd

def read_df(p: Path) -> pd.DataFrame:
    return pd.read_csv(
        p, sep="|", header=None, encoding="latin-1",
        quotechar='"', on_bad_lines="skip", dtype=str
    )

def save_df(df: pd.DataFrame, p: Path):
    df.to_csv(p, index=False)   

def parse(input_path: Path, output_path: Path) -> pd.DataFrame:
    if not input_path.exists():
        print(input_path)
        raise FileNotFoundError(f"File not found: {input_path}")
    print(f"Loading data from: {input_path}")
    df = read_df(input_path)
    print(df.head())
    print(f"Saving processed data to: {output_path}")
    save_df(df, output_path)
    return df

def merge_products_purposes():
    base = Path(__file__).resolve().parent.parent / "DataBase"

    products_df = parse(base/"NHP_PRODUCTS.txt",         base/"NHP_PRODUCTS.csv")
    purposes_df = parse(base/"NHP_PRODUCTS_PURPOSE.txt", base/"NHP_PRODUCTS_PURPOSE.csv")

    merged = pd.merge(products_df, purposes_df, on=0, how="inner")

    merged_out = base / "merged_products_purposes.csv"
    save_df(merged, merged_out)
    print(f"Merged saved to: {merged_out}")

    slim = merged[["2_x", "1_y"]].copy()
    slim.columns = ["name", "description"]
    slim = slim.replace(r"^\s*$", pd.NA, regex=True).dropna()

    slim_out = base / "products_with_purpose.csv"
    save_df(slim, slim_out)
    print(f"Slim version saved to: {slim_out}")
