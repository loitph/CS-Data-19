from decimal import Decimal

gross_avenue = Decimal(input("Enter the gross avenue: "))
forcasting_rate = Decimal(input("Enter the forcasting rate (as a decimal): "))

forcasting_yearly = int(input("Enter the number of years for forecasting: "))

future_gross_avenue_next_years = gross_avenue * (1 + forcasting_rate) ** forcasting_yearly

print(f'Future Gross Avenue in {forcasting_yearly} years: ${future_gross_avenue_next_years:,.2f}')