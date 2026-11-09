import os
import json
import pandas as pd

from src.product import Product

product = Product()

def store_as_json() -> None:
  os.makedirs(product.data_dir, exist_ok=True)

  path = os.path.join(product.data_dir, "product_management.json")

  data = [{**p, "price_import": float(p["price_import"]), "price_export": float(p["price_export"])} for p in product.products]

  with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

  print(f"Saved {len(data)} product(s) to {path}")

def store_as_excel() -> None:
  os.makedirs(product.data_dir, exist_ok=True)

  path = os.path.join(product.data_dir, "product_management.xlsx")

  df = pd.DataFrame(product.products, columns=["name", "price_import", "price_export", "quantity"])

  df["price_import"] = df["price_import"].astype(float)
  df["price_export"] = df["price_export"].astype(float)

  df["total_import"] = df["price_import"] * df["quantity"]
  df["total_export"] = df["price_export"] * df["quantity"]

  df["gross_value"] = df["price_export"] * df["quantity"]

  df["net_profit"] = df["price_import"] * df["quantity"]

  df["revenue"] = df["gross_value"] - df["net_profit"]

  df.to_excel(path, index=False)

  print(f"Saved {len(df)} product(s) to {path}")