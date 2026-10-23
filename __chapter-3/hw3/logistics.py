from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
import os
from copy import copy
from decimal import Decimal

excel_file = "logistics.xlsx"

if os.path.exists(excel_file):
  workbook = load_workbook(excel_file)
  worksheet = workbook.worksheets[0]
else:
  workbook = Workbook()
  worksheet = workbook.worksheets[0]

for row_index, row in enumerate(worksheet.iter_rows(values_only=True), start=1):
  if row_index == 1:
    continue
  weight, fee, shipping_type, depart, arrive = row[5], row[7], row[6], row[3], row[4]
  if weight is None or fee is None or shipping_type is None or depart is None or arrive is None:
    continue

  weight = Decimal(weight)
  fee = Decimal(fee)
  type_of_cost = ""

  cost = weight * fee
  super_fast = "Siêu tốc"
  
  if 5 < weight <= 20:
    cost = cost * Decimal("0.95")
  elif weight > 20:
    cost = cost * Decimal("0.90")
  else:
    cost = cost

  if shipping_type == super_fast:
    cost += 20_000

  north_side = ["Hà Nội", "Hải Phòng", "Nam Định"]
  mid_side = ["Đà Nẵng", "Huế"]
  south_side = ["TP.HCM", "Cần Thơ", "Vũng Tàu"]

  if depart in north_side and arrive in north_side or depart in mid_side and arrive in mid_side or depart in south_side and arrive in south_side:
    cost = cost * Decimal("0.95")

  if cost > 500_000:
    type_of_cost = "Cao"
  elif 200_000 < cost <= 500_000:
    type_of_cost = "Trung bình"
  else:
    type_of_cost = "Thấp"

  cell_cost = worksheet.cell(row=row_index, column=9, value=(
    cost
  ))
  cell_cost._style = copy(worksheet.cell(row=row_index, column=1)._style)
  # format cell #,##0
  cell_cost.number_format = '#,##0'

  # write title for this column
  title_type_of_cost = worksheet.cell(row=1, column=10, value="Phân loại cước")
  cell_type_of_cost = worksheet.cell(row=row_index, column=10, value=(
    type_of_cost
  ))
  cell_type_of_cost._style = copy(worksheet.cell(row=row_index, column=1)._style)
  title_type_of_cost._style = copy(worksheet.cell(row=1, column=1)._style)

# widen the profit type / profit columns
worksheet.column_dimensions[get_column_letter(9)].width = 22
worksheet.column_dimensions[get_column_letter(10)].width = 15


workbook.save(excel_file)
print(f'Excel file "{excel_file}" updated successfully.')