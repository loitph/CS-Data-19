from openpyxl import Workbook

excel_file = 'test-flight-1.xlsx'

read_workbook = Workbook()
worksheet = read_workbook.active

worksheet.title = 'Flight Data'

new_headers = [
  'Flight Number',
  'Departure',
  'Arrival',
  'Duration',
  'Price'
]

worksheet.append(new_headers)

worksheet.append([
  'AA123',
  'New York',
  'Los Angeles',
  '6h 15m',
  350
])

read_workbook.save(excel_file)
print(f'Excel file "{excel_file}" created successfully with flight data.')