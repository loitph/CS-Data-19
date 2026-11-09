import os
import json
from decimal import Decimal

class Product:
  _instance = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self):
    self._instance.products = []
    self._instance.data_dir = os.path.join(
      os.path.dirname(
        os.path.dirname(
          os.path.abspath(__file__)
        )
      ), "data"
    )
    self._instance.load_from_store()


  def load_from_store(self) -> None:
    path = os.path.join(self.data_dir, "product_management.json")

    if not os.path.exists(path):
      return

    with open(path, "r", encoding="utf-8") as f:
      data = json.load(f)

    self.products = [
      {
        **p, "price_import": Decimal(str(p["price_import"])), "price_export": Decimal(str(p["price_export"]))
      } for p in data
    ]

  products: list[dict]
  data_dir: str