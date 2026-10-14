import os
import re
from decimal import Decimal, InvalidOperation
from openpyxl import Workbook

class Student:
  def __init__(self, name: str, avg_score: Decimal):
    self.name = name
    self.avg_score = avg_score
    self.ranking = self.__ranking__()

  def __ranking__(self) -> str:
    if self.avg_score >= 8:
      return 'Excellent'
    elif self.avg_score >= 6:
      return 'Good'
    elif self.avg_score >= 4:
      return 'Pass'
    else:
      return 'Fail'

  def __to_row__(self) -> list[str | Decimal]:
    return [self.name, self.avg_score, self.ranking]

  def get_row(self) -> list[str | Decimal]:
    return self.__to_row__()

menu_title = "\n--- Menu ---"
opt_1_info = "1. Enter the student's name, average score"
opt_2_report = "2. Print the report"
opt_3_exit = "3. Exit"
menu_end = "--- #### ---\n"

msg_choice = "Enter your choice: "
msg_err_choice = "Invalid choice. Please enter a number between 1 and 3.\n"

msg_name = "Enter the student's name: "
msg_err_name = "Invalid name. Letters and spaces only.\n"

msg_avg_score = "Enter the student's average score: "
msg_err_avg_score = "Invalid input. Please enter a valid average score.\n"


goodbye = "Goodbye!"

WORDS_PATTERN = re.compile(r"[^\W\d_]+(?: [^\W\d_]+)*")

lst_sdt = []

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

def avg_score_input(prompt: str) -> Decimal:
  while True:
    avg_score = safe_parse_decimal(input(prompt))
    if avg_score is not None and 0 <= avg_score <= 10:
      return avg_score
    print(msg_err_avg_score)

def save_to_excel() -> None:
  excel_file = 'report-student-ranking.xlsx'

  if not lst_sdt:
    print('No new data to save.')
    return

  if os.path.exists(excel_file):
    workbook = load_workbook(excel_file)
    worksheet = workbook.active
  else:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Student Ranking Report'
    worksheet.append([
      'No.',
      'Student Name',
      'Average Score',
      'Ranking'
    ])

  start_no = worksheet.max_row
  for i, row in enumerate(lst_sdt, start=start_no):
    worksheet.append([i, *row])

  workbook.save(excel_file)
  print(f'Saved {len(lst_sdt)} new row(s) to "{excel_file}".')

  lst_sdt.clear()

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
      name = name_input(msg_name)
      avg_score = avg_score_input(msg_avg_score)
      lst_sdt.append(Student(name, avg_score).get_row())
    elif choice == 2:
      save_to_excel()
    else:
      print(msg_err_choice)


if __name__ == "__main__":
  main()