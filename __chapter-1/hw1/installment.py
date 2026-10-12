loan_amount = 1_000_000
loan_interest_rate_per_year = 0.12
loan_term_in_years = 2

# calculate the total amount to be paid back each month
EMI = loan_amount * (loan_interest_rate_per_year / 12) * (1 + loan_interest_rate_per_year / 12) ** (loan_term_in_years * 12) / ((1 + loan_interest_rate_per_year / 12) ** (loan_term_in_years * 12) - 1)
print(f'EMI: ${EMI:,.2f}')