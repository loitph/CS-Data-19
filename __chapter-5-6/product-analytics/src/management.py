from decimal import Decimal, InvalidOperation
from src.product import Product

msg_err_choice = "Invalid choice. Please enter a number between 1 and {}.\n"
msg_err_number = "Invalid input. Please enter a valid number.\n"
msg_err_non_negative = "Invalid input. Please enter a valid number greater than or equal to 0.\n"
msg_err_int = "Invalid input. Please enter a whole number greater than or equal to {}.\n"

product = Product()

def safe_parse_int(s: str) -> int | None:
  try:
    return int(s.strip().replace("_", "").replace(",", ""))
  except ValueError:
    return None

def safe_parse_decimal(s: str) -> Decimal | None:
  try:
    d = Decimal(s.strip().replace("_", "").replace(",", ""))
  except InvalidOperation:
    return None
  if not d.is_finite():
    return None
  return d

def choice_input(prompt: str, max_choice: int) -> int:
  while True:
    choice = safe_parse_int(input(prompt))
    if choice is not None and 1 <= choice <= max_choice:
      return choice
    print(msg_err_choice.format(max_choice))

def number_input(prompt: str, default: Decimal | None = None, allow_negative: bool = False) -> Decimal:
  while True:
    raw = input(prompt)
    if not raw.strip() and default is not None:
      return default
    value = safe_parse_decimal(raw)
    if value is not None and (allow_negative or value >= 0):
      return value
    print(msg_err_number if allow_negative else msg_err_non_negative)

def int_input(prompt: str, minimum: int = 0) -> int:
  while True:
    value = safe_parse_int(input(prompt))
    if value is not None and value >= minimum:
      return value
    print(msg_err_int.format(minimum))

def import_product() -> None:
  name = input("Enter the product name: ")
  price_import = number_input("Enter the product price import: ", default=Decimal(0), allow_negative=True)
  price_export = number_input("Enter the product price export: ", default=Decimal(0), allow_negative=True)
  quantity = int_input("Enter the product quantity: ", minimum=0)

  prod = {"name": name, "price_import": price_import, "price_export": price_export, "quantity": quantity}
  product.products.append(prod)
  print(f"Product added: {prod}")

def list_products() -> None:
  print("List of products:")
  for prod in product.products:
    print(prod)