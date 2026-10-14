import os
from decimal import Decimal, InvalidOperation
from typing import Callable

menu_title = "\n--- Menu ---"
section_class = "I. Exercises"
section_homework = "II. Homework"
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

def yes_no_input(prompt: str) -> bool:
  while True:
    answer = input(prompt).strip().lower()
    if answer in ("yes", "y"):
      return True
    if answer in ("no", "n"):
      return False
    print(msg_err_yes_no)

def fmt_vnd(amount: Decimal) -> str:
  return f"{amount:,.0f} VND"

def fmt_usd(amount: Decimal) -> str:
  return f"{amount:,.2f} USD"

def profit_or_loss() -> None:
  revenue = number_input("Enter revenue (USD): ", default=Decimal(120_000))
  cost = number_input("Enter total cost (USD): ", default=Decimal(130_000))
  profit = revenue - cost

  if profit > 0:
    print(f"Profit: the profit amount is {fmt_usd(profit)}")
  elif profit < 0:
    print(f"Loss: the loss amount is {fmt_usd(abs(profit))}")
  else:
    print("No profit, no loss")

def loan_eligibility() -> None:
  income = number_input("Enter monthly income (VND): ")
  has_debt = yes_no_input("Do you have any current debt? (Yes/No): ")

  if income >= 100_000_000 and not has_debt:
    print("Eligible for loan")
  else:
    print("Not eligible for loan")

def personal_income_tax() -> None:
  # income <= 10M -> 5%
  # 10M < income <= 20M -> 10%
  # income > 20M -> 15%
  income = number_input("Enter monthly income T (VND): ")

  if income <= 10_000_000:
    rate = Decimal("0.05")
  elif income <= 20_000_000:
    rate = Decimal("0.10")
  else:
    rate = Decimal("0.15")

  tax = income * rate
  print(f"Tax rate: {rate:.0%}")
  print(f"Tax payable = {fmt_vnd(tax)}")

def savings_interest() -> None:
  # months <= 6 -> 4%/year
  # 6 < months <= 12 -> 5%/year
  # months > 12 -> 6%/year
  # total = P * (1 + r * months / 12)
  principal = number_input("Enter deposit amount P (VND): ")
  months = int_input("Enter deposit term (months): ", minimum=1)

  if months <= 6:
    rate = Decimal("0.04")
  elif months <= 12:
    rate = Decimal("0.05")
  else:
    rate = Decimal("0.06")

  total = principal * (1 + rate * months / 12)
  print(f"Interest rate: {rate:.0%}/year")
  print(f"Total amount = {fmt_vnd(total)}")

def credit_approval() -> None:
  # bad debt -> rejected
  # no bad debt, income > 15M -> approved
  # no bad debt, income <= 15M -> needs review
  income = number_input("Enter monthly income T (VND): ")
  has_bad_debt = yes_no_input("Do you have any bad debt? (Yes/No): ")

  if has_bad_debt:
    print("Rejected")
  elif income > 15_000_000:
    print("Approved")
  else:
    print("Needs review")


# ---------- Homework ----------

def year_end_bonus() -> None:
  # revenue > 1,000,000 -> 5%
  # 500,000 <= revenue <= 1,000,000 -> 3%
  # revenue < 500,000 -> 0
  revenue = number_input("Enter revenue (USD): ")

  if revenue > 1_000_000:
    bonus = revenue * Decimal("0.05")
  elif revenue >= 500_000:
    bonus = revenue * Decimal("0.03")
  else:
    bonus = Decimal(0)

  print(f"Bonus = {fmt_usd(bonus)}")

def profit_classification() -> None:
  # profit > 100,000 -> high
  # 50,000 <= profit <= 100,000 -> medium
  # profit < 50,000 -> low
  profit = number_input("Enter profit after tax (USD): ", allow_negative=True)

  if profit > 100_000:
    print("High profit")
  elif profit >= 50_000:
    print("Medium profit")
  else:
    print("Low profit")

def production_cost() -> None:
  # total = fixed + quantity * variable
  # total > 500,000,000 -> 10% discount
  FIXED_COST = Decimal(100_000_000)
  VARIABLE_COST = Decimal(50_000)
  DISCOUNT_THRESHOLD = Decimal(500_000_000)

  quantity = int_input("Enter number of products N: ")
  total = FIXED_COST + quantity * VARIABLE_COST

  if total > DISCOUNT_THRESHOLD:
    total = total * Decimal("0.9")
    discounted = "Yes"
  else:
    discounted = "No"

  print(f"Total cost = {fmt_vnd(total)}, Discount applied = {discounted}")

def budget_allocation() -> None:
  # cost A > 50M -> A gets 40% of budget, else 0
  # cost B > 30M -> B gets 30% of budget, else 0
  # C gets the rest
  budget = number_input("Enter budget B1 (VND): ")
  cost_a = number_input("Enter project A cost (VND): ")
  cost_b = number_input("Enter project B cost (VND): ")
  cost_c = number_input("Enter project C cost (VND): ")

  amount_a = budget * Decimal("0.4") if cost_a > 50_000_000 else Decimal(0)
  amount_b = budget * Decimal("0.3") if cost_b > 30_000_000 else Decimal(0)
  amount_c = budget - (amount_a + amount_b)

  print(f"Allocated to A = {fmt_vnd(amount_a)}")
  print(f"Allocated to B = {fmt_vnd(amount_b)}")
  print(f"Allocated to C = {fmt_vnd(amount_c)} (requested: {fmt_vnd(cost_c)})")

def credit_score() -> None:
  # income: > 20M -> 50, 10M-20M -> 30, < 10M -> 10
  # years: > 5 -> 30, 1-5 -> 20, < 1 -> 10
  # total >= 70 -> Good, 50-69 -> Fair, < 50 -> Weak
  income = number_input("Enter monthly income (VND): ")
  years = number_input("Enter years using bank services: ")

  if income > 20_000_000:
    income_points = 50
  elif income >= 10_000_000:
    income_points = 30
  else:
    income_points = 10

  if years > 5:
    years_points = 30
  elif years >= 1:
    years_points = 20
  else:
    years_points = 10

  total = income_points + years_points

  if total >= 70:
    rank = "Good"
  elif total >= 50:
    rank = "Fair"
  else:
    rank = "Weak"

  print(f"Total score = {total}, Rank = {rank}")


CLASS_EXERCISES: list[tuple[str, Callable[[], None]]] = [
  ("Profit or Loss Assessment", profit_or_loss),
  ("Loan Eligibility", loan_eligibility),
  ("Personal Income Tax", personal_income_tax),
  ("Savings Deposit Interest", savings_interest),
  ("Credit Approval Check", credit_approval),
]

HOMEWORKS: list[tuple[str, Callable[[], None]]] = [
  ("Year-end Bonus", year_end_bonus),
  ("Profit Classification", profit_classification),
  ("Production Cost", production_cost),
  ("Investment Budget Allocation", budget_allocation),
  ("Credit Score", credit_score),
]

ACTIONS = CLASS_EXERCISES + HOMEWORKS
EXIT_CHOICE = len(ACTIONS) + 1

def print_menu() -> None:
  print(menu_title)
  for i, (title, _) in enumerate(CLASS_EXERCISES, start=1):
    print(f"{i:>2}. {title}")
  print(section_homework)
  for i, (title, _) in enumerate(HOMEWORKS, start=len(CLASS_EXERCISES) + 1):
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
