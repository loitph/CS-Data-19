from openpyxl import Workbook

excel_file = 'employee-management.xlsx'

workbook = Workbook()
worksheet = workbook.active

worksheet.title = 'Employee Management'

new_headers = [
  'Employee ID',
  'Employee Name',
  'Role',
  'Salary'
]

worksheet.append(new_headers)

employee_data = [
  ['E001', 'John Doe', 'Software Engineer', 80_000],
  ['E002', 'Jane Smith', 'Data Analyst', 70_000],
  ['E003', 'Bob Johnson', 'Project Manager', 90_000],
  ['E004', 'Alice Williams', 'UX Designer', 60_000],
  ['E005', 'Charlie Brown', 'Database Administrator', 85_000]
]

for employee in employee_data:
    worksheet.append(employee)

workbook.save(excel_file)
print(f'Excel file "{excel_file}" created successfully with employee management data.')