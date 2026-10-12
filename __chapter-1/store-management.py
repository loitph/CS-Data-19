from openpyxl import Workbook

excel_file = 'management.xlsx'

workbook = Workbook()
worksheet = workbook.active

worksheet.title = 'Store Management'

new_headers = [
  'Product Code',
  'Product Name',
  'Price'
]

worksheet.append(new_headers)

worksheet.append([
  '1234',
  'New York',
  'John Doe'
])

workbook.save(excel_file)
print(f'Excel file "{excel_file}" created successfully with store management data.')