import os
import re
from decimal import Decimal, InvalidOperation
from openpyxl import Workbook, load_workbook

class People:
  def __init__(self, name: str, kWh: Decimal, total: Decimal):
    self.name = name
    self.kWh = kWh
    self.total = total

  def __str__(self) -> str:
    return f"{self.name}, {self.kWh}, {self.total}"

  def __to_row__(self) -> list[str | Decimal]:
    return [self.name, self.kWh, self.total]

  def get_row(self) -> list[str | Decimal]:
    return self.__to_row__()


menu_title = "\n--- Menu ---"
opt_1_info = "1. Enter the customer's name, kWh used, usage allowance, total amount"
opt_2_report = "2. Print the report"
opt_3_exit = "3. Exit"
menu_end = "--- #### ---\n"

msg_choice = "Enter your choice: "
msg_err_choice = "Invalid choice. Please enter a number between 1 and 3.\n"

msg_customer_name = "Enter the customer's name: "
msg_err_name = "Invalid name. Letters and spaces only.\n"
msg_kWh = "Enter the number of kilowatt-hours (kWh) used: "
msg_err_kWh = "Invalid input. Please enter a valid kilowatt-hours (kWh).\n"

goodbye = "Goodbye!"

WORDS_PATTERN = re.compile(r"[^\W\d_]+(?: [^\W\d_]+)*")

lst_ppl = []

def safe_input_name(s: str) -> str | None:
  s = " ".join(s.split())
  if WORDS_PATTERN.fullmatch(s):
    return s
  return None

def safe_parse_int(s: str) -> int | None:
  try:
    return int(s)
  except ValueError:
    return None

def safe_parse_decimal(s: str) -> Decimal | None:
  try:
    d = Decimal(s.strip())
  except InvalidOperation:
    return None
  if not d.is_finite():
    return None
  return d

def choice_input(prompt: str) -> str:
  while True:
    s = input(prompt)
    if safe_parse_int(s) is not None and isinstance(safe_parse_int(s), int) and 1 <= safe_parse_int(s) <= 3:
        return int(s)
    else:
      print(msg_err_choice)

def name_input(prompt: str) -> str:
  while True:
    name = input(prompt)
    if safe_input_name(name) is not None:
      return safe_input_name(name)
    else:
      print(msg_err_name)

def kilowatt_input(prompt: str) -> Decimal:
  while True:
    kWh = safe_parse_decimal(input(prompt))
    if kWh is not None and kWh >= 0:
      return kWh
    print(msg_err_kWh)

def calc_total(kWh: Decimal) -> Decimal:
  # 0 <= kWh <= 50 -> 1_800VND/kWh
  # 51 <= kWh <= 100 -> 2_000VND/kWh
  # 101 <= kWh <= 200 -> 2_500VND/kWh
  # kWh > 200 -> 3_000VND/kWh

  TIERS = [
    (Decimal(50), 1_800),
    (Decimal(100), 2_000),
    (Decimal(200), 2_500),
    (Decimal('Infinity'), 3_000),
  ]

  total = Decimal(0)
  prev_limit = Decimal(0)

  for limit, rate in TIERS:
    if kWh <= prev_limit:
      break
    total += (min(kWh, limit) - prev_limit) * rate
    prev_limit = limit

  return total

def save_to_excel() -> None:
  excel_file = 'report-electricity-bill.xlsx'

  if not lst_ppl:
    print('No new data to save.')
    return

  if os.path.exists(excel_file):
    workbook = load_workbook(excel_file)
    worksheet = workbook.active
  else:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Electricity Bill Report'
    worksheet.append([
      'No.',
      'Customer Name',
      'kWh Used',
      'Total Amount (VND)'
    ])

  start_no = worksheet.max_row
  for i, row in enumerate(lst_ppl, start=start_no):
    worksheet.append([i, *row])

  workbook.save(excel_file)
  print(f'Saved {len(lst_ppl)} new row(s) to "{excel_file}".')

  lst_ppl.clear()


def main() -> None:
  os.system('cls' if os.name == 'nt' else 'clear')
  while True:
    print(menu_title)
    print(opt_1_info)
    print(opt_2_report)
    print(opt_3_exit)
    print(menu_end)

    choice = choice_input(msg_choice)

    if choice == 3:
      print(goodbye)
      break
    elif choice == 1:
      name = name_input(msg_customer_name)
      kWh = kilowatt_input(msg_kWh)
      total = calc_total(kWh)
      lst_ppl.append(People(name, kWh, total).get_row())
    elif choice == 2:
      save_to_excel()
    else:
      print(msg_err_choice)

if __name__ == "__main__":
  main()