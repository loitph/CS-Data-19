from decimal import Decimal

gross_revenue = Decimal(input("Enter the gross revenue: "))
cost_of_goods_sold = Decimal(input("Enter the cost of goods sold: "))

gross_profit = gross_revenue - cost_of_goods_sold
gross_profit_margin = (gross_profit / gross_revenue) * 100

print(f'Gross Profit: ${gross_profit:,.2f}')
print(f'Rate of Gross Profit: {gross_profit_margin:.2f}%')