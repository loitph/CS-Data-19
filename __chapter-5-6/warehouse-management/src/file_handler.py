import os
import json
import pandas as pd

from src.store import ProductStore

store = ProductStore()

def store_as_json() -> None:
  # ./data/store_management.json
  os.makedirs(store.data_dir, exist_ok=True)

  path = os.path.join(store.data_dir, "store_management.json")

  data = [{**p, "price": float(p["price"])} for p in store.products]

  with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

  print(f"Saved {len(data)} product(s) to {path}")

def store_as_excel() -> None:
  # ./data/store_management.xlsx
  os.makedirs(store.data_dir, exist_ok=True)

  path = os.path.join(store.data_dir, "store_management.xlsx")

  df = pd.DataFrame(store.products, columns=["name", "price", "quantity"])

  df["price"] = df["price"].astype(float)

  df["total"] = df["price"] * df["quantity"]

  df.to_excel(path, index=False)

  print(f"Saved {len(df)} product(s) to {path}")
