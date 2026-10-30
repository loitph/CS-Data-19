import os
import json
from decimal import Decimal


class ProductStore:
  """Singleton holding the shared product list and data directory."""

  _instance: "ProductStore | None" = None

  def __new__(cls) -> "ProductStore":
    if cls._instance is None:
      cls._instance = super().__new__(cls)
      cls._instance.products = []
      cls._instance.data_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
      )
      cls._instance.load_from_store()
    return cls._instance

  def load_from_store(self) -> None:
    path = os.path.join(self.data_dir, "store_management.json")

    if not os.path.exists(path):
      return

    with open(path, "r", encoding="utf-8") as f:
      data = json.load(f)

    self.products = [
      {
        **p, "price": Decimal(str(p["price"]))
      } for p in data
    ]

  products: list[dict]
  data_dir: str
