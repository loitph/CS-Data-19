from decimal import Decimal

invest = Decimal(input("Enter the investment amount: "))
gross_revenue = Decimal(input("Enter the gross revenue: "))

roi = (gross_revenue - invest) / invest
roi_percentage = roi * 100

print(f'ROI: {roi_percentage:,.2f}%')