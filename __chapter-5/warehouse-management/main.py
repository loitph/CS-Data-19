import os
from typing import Callable

from src.management import add_product, list_products, choice_input
from src.file_handler import store_as_json, store_as_excel
from src.store import ProductStore

menu_title = "\n--- Menu ---"
menu_end = "--- #### ---\n"

msg_choice = "Enter your choice: "

goodbye = "Goodbye!"

MENU: list[tuple[str, Callable[[], None]]] = [
  ("Add Product", add_product),
  ("List Products", list_products),
  ("Store as JSON", store_as_json),
  ("Store as Excel", store_as_excel),
]

EXIT_CHOICE = len(MENU) + 1

def print_menu() -> None:
  print(menu_title)
  for i, (title, _) in enumerate(MENU, start=1):
    print(f"{i:>2}. {title}")
  print(f"{EXIT_CHOICE:>2}. Exit")
  print(menu_end)


def main() -> None:
  ProductStore()
  os.system('cls' if os.name == 'nt' else 'clear')
  while True:
    print_menu()

    choice = choice_input(msg_choice, EXIT_CHOICE)

    if choice == EXIT_CHOICE:
      print(goodbye)
      break

    title, action = MENU[choice - 1]
    print(f"\n========= {title} =========")
    action()
    print("======================================")

if __name__ == "__main__":
  main()
