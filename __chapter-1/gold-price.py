
# Cong ty vang PNJ, DOJI, Mi Hong
# [cong ty, ngay, gia ban ra, mua vao, loai vang]


from openpyxl import Workbook

excel_file = 'gold-price.xlsx'

workbook = Workbook()
worksheet = workbook.active

worksheet.title = 'Gold Price'

new_headers = [
  'Company',
  'Date',
  'Sell Price',
  'Buy Price',
  'Gold Type',
  'Units'
]

worksheet.append(new_headers)

data = [
  ['PNJ', '2026-10-12', 140_800_000, 143_800_000, 'PNJ', 'Bar'],
  ['DOJI', '2026-10-12', 138_500_000, 141_500_000, '9999', 'Bar'],
  ['Mi Hong', '2026-10-12', 141_300_000, 142_800_000, '999', 'Bar']
]

for row in data:
    worksheet.append(row)

workbook.save(excel_file)
print(f'Excel file "{excel_file}" created successfully with gold price data.')