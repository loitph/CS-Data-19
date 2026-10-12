from decimal import Decimal

loan_amount = Decimal(input("Enter the loan amount: "))
loan_interest_rate_per_year = Decimal(input("Enter the loan interest rate per year (as a decimal): "))
loan_term_in_years = int(input("Enter the loan term in years: "))

# calculate the total amount to be paid back each month
EMI = loan_amount * (loan_interest_rate_per_year / 12) * (1 + loan_interest_rate_per_year / 12) ** (loan_term_in_years * 12) / ((1 + loan_interest_rate_per_year / 12) ** (loan_term_in_years * 12) - 1)
print(f'EMI: ${EMI:,.2f}')