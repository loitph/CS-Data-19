import os
import re
import unicodedata
from collections.abc import Callable

from src.db import close_engine

Action = tuple[str, Callable[[], None]]

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


def to_snake_case(name: str) -> str:
  name = name.replace("đ", "d").replace("Đ", "D")
  ascii_name = (
    unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
  )
  return re.sub(r"[^a-z0-9]+", "_", ascii_name.lower()).strip("_")


def clear_screen() -> None:
  os.system("cls" if os.name == "nt" else "clear")


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


def print_menu(actions: list[Action]) -> None:
  print(menu_title)
  for i, (title, _) in enumerate(actions, start=1):
    print(f"{i:>2}. {title}")
  print(f"{len(actions) + 1:>2}. Exit")
  print(menu_end)


def run_menu(actions: list[Action]) -> None:
  exit_choice = len(actions) + 1
  clear_screen()
  try:
    while True:
      print_menu(actions)

      choice = choice_input(msg_choice, exit_choice)

      if choice == exit_choice:
        print(goodbye)
        break

      title, action = actions[choice - 1]
      print(f"\n========= {title} =========")
      action()
      print("======================================")
  finally:
    close_engine()
