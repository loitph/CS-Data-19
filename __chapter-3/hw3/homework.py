import os
from decimal import Decimal, InvalidOperation
from typing import Callable

menu_title = "\n--- Menu ---"
menu_end = "--- #### ---\n"

msg_choice = "Enter your choice: "
msg_err_choice = "Invalid choice. Please enter a number between 1 and {}.\n"
msg_err_number = "Invalid input. Please enter a valid number.\n"
msg_err_non_negative = "Invalid input. Please enter a valid number greater than or equal to 0.\n"
msg_err_int = "Invalid input. Please enter a whole number greater than or equal to {}.\n"
msg_err_yes_no = "Invalid input. Please enter Yes or No.\n"

goodbye = "Goodbye!"

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


def second_greatest() -> None:
  string_number_array = input("Enter a list of numbers separated by a comma: ").split(",")

  number_array = [int(num) for num in string_number_array]

  number_array.sort(reverse=True)

  print(f"The second greatest number in the list is: {number_array[1]}")
  return

def distinguish_odd_even() -> None:
  list_any_number = input("Enter a list of numbers separated by a comma: ").split(",")

  dict_any_number = {num: int(num) for num in list_any_number}

  for key, value in dict_any_number.items():
    if value % 2 == 0:
      print(f"{key} is even")
    else:
      print(f"{key} is odd")
  return

def find_greater_or_equal_number() -> None:
  list_any_number = input("Enter a list of numbers separated by a comma: ").split(",")

  number_barrier = int_input("Enter the barrier number: ", minimum=-10**9)

  numbers = [int(num) for num in list_any_number if num.strip()]

  for num in numbers:
    if num >= number_barrier:
      print(f"{num} is greater or equal to {number_barrier}")
  return


def bubble_sort(num_arr: list[int]) -> list[int]:
  len_arr = len(num_arr)
  for cursor_idx in range(len_arr):
    for idx in range(0, len_arr - cursor_idx - 1):
      if num_arr[idx] > num_arr[idx + 1]:
        num_arr[idx], num_arr[idx + 1] = num_arr[idx + 1], num_arr[idx]

  return num_arr

def ascending_order() -> None:
  list_any_number = input("Enter a list of numbers separated by a comma: ").split(",")

  number_array = [int(num) for num in list_any_number]

  bubble_sort(number_array)

  print(f"The list in ascending order is: {number_array}")

  return

def linear_search() -> None:
  list_any_number = input("Enter a list of numbers separated by a comma: ").split(",")

  number_array = [int(num) for num in list_any_number]

  number_barrier = int_input("Enter the barrier number: ", minimum=-10**9)

  for num in number_array:
    if num == number_barrier:
      return print(f"{num} is in the list")

  return print(f"{number_barrier} is not in the list")


HOMEWORKS: list[tuple[str, Callable[[], None]]] = [
  ("The Second Greatest in Integer Array", second_greatest),
  ("Distinguish Odd and Even", distinguish_odd_even),
  ("Find the greater or equal number", find_greater_or_equal_number),
  ("Ascending order", ascending_order),
  ("Linear search", linear_search),
]

ACTIONS = HOMEWORKS
EXIT_CHOICE = len(ACTIONS) + 1

def print_menu() -> None:
  print(menu_title)
  for i, (title, _) in enumerate(HOMEWORKS, start=1):
    print(f"{i:>2}. {title}")
  print(f"{EXIT_CHOICE:>2}. Exit")
  print(menu_end)


def main() -> None:
  os.system('cls' if os.name == 'nt' else 'clear')
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