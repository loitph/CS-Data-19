from decimal import Decimal, InvalidOperation

from src.store import ProductStore

store = ProductStore()

def profit_analysis() -> None:
  total_profit = Decimal(0)
  for product in store.products:
    total_profit += product["price"] * product["quantity"]
  print(f"Total profit: {total_profit}")