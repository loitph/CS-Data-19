import os
from decimal import Decimal, InvalidOperation
from typing import Callable

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from dotenv import load_dotenv


menu_title = "\n--- Menu ---"
menu_end = "--- #### ---\n"

msg_choice = "Enter your choice: "
msg_err_choice = "Invalid choice. Please enter a number between 1 and {}.\n"
msg_err_number = "Invalid input. Please enter a valid number.\n"
msg_err_non_negative = (
  "Invalid input. Please enter a valid number greater than or equal to 0.\n"
)
msg_err_int = (
  "Invalid input. Please enter a whole number greater than or equal to {}.\n"
)
msg_err_yes_no = "Invalid input. Please enter Yes or No.\n"

goodbye = "Goodbye!"


def safe_parse_int(s: str) -> int | None:
  try:
    return int(s.strip().replace("_", "").replace(",", ""))
  except ValueError:
    return None


def choice_input(prompt: str, max_choice: int) -> int:
  while True:
    choice = safe_parse_int(input(prompt))
    if choice is not None and 1 <= choice <= max_choice:
      return choice
    print(msg_err_choice.format(max_choice))


def int_input(prompt: str, minimum: int = 0) -> int:
  while True:
    value = safe_parse_int(input(prompt))
    if value is not None and value >= minimum:
      return value
    print(msg_err_int.format(minimum))


def initial_data() -> None:
  pass


def analysis_numbers() -> None:
  pass


ACTIONS: list[tuple[str, Callable[[], None]]] = [
  ("Initial data", initial_data),
  ("Analysis of the rate of numbers", analysis_numbers),
]
EXIT_CHOICE = len(ACTIONS) + 1


def print_menu() -> None:
  print(menu_title)
  for i, (title, _) in enumerate(ACTIONS, start=1):
    print(f"{i:>2}. {title}")
  print(f"{EXIT_CHOICE:>2}. Exit")
  print(menu_end)


def main() -> None:
  os.system("cls" if os.name == "nt" else "clear")
  while True:
    print_menu()

    choice = choice_input(msg_choice, EXIT_CHOICE)

    if choice == EXIT_CHOICE:
      print(goodbye)
      break

    title, action = ACTIONS[choice - 1]
    print(f"\n========= {title} =========")
    action()
    print("======================================")


if __name__ == "__main__":
  main()
