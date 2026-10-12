from decimal import Decimal

gross_avenue = Decimal(input("Enter the gross avenue: "))
forcasting_rate = Decimal(input("Enter the forcasting rate (as a decimal): "))

future_gross_avenue_next_5_years = gross_avenue * (1 + forcasting_rate) ** 5

print(f'Future Gross Avenue in 5 years: ${future_gross_avenue_next_5_years:,.2f}')