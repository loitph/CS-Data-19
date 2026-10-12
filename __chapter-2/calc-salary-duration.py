from decimal import Decimal

gross_salary_per_hour = Decimal(input("Enter the gross salary per hour: "))
total_working_hours = Decimal(input("Enter the total working hours: "))

# Solution 1: Using integer division and modulo
base_working_hours = total_working_hours // 40
overtime_working_hours = total_working_hours % 40

# Solution 2: Using conditional statements
# if total_working_hours > 40:
#     base_working_hours = 40
#     overtime_working_hours = total_working_hours - 40
# else:
#     base_working_hours = total_working_hours
#     overtime_working_hours = 0

total_salary = (base_working_hours * gross_salary_per_hour * 40) + (overtime_working_hours * gross_salary_per_hour * 2)

print(f"Total salary: ${total_salary:.2f}")