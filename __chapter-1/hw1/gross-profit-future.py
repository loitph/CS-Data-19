gross_avenue = 50_000
forcasting_rate = 0.05
future_gross_avenue_next_5_years = gross_avenue * (1 + forcasting_rate) ** 5
print(f'Future Gross Avenue in 5 years: ${future_gross_avenue_next_5_years:,.2f}')