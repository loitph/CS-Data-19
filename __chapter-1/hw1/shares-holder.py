from decimal import Decimal

net_revenue = Decimal(input("Enter the net revenue: "))
number_of_common_shares = Decimal(input("Enter the number of common shares: "))

dividend_rate_per_share = Decimal(input("Enter the dividend rate per share (as a decimal): "))

earnings_per_share = net_revenue / number_of_common_shares

# total_dividend = number_of_common_shares * earnings_per_share * dividend_rate_per_share

total_dividend = number_of_common_shares * (earnings_per_share * dividend_rate_per_share)

print(f'Total Dividend: ${total_dividend:,.2f}')