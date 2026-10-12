net_revenue = 1_200_000
number_of_common_shares = 20_000

dividend_rate_per_share = 0.15

earnings_per_share = net_revenue / number_of_common_shares

# total_dividend = number_of_common_shares * earnings_per_share * dividend_rate_per_share

total_dividend = number_of_common_shares * (earnings_per_share * dividend_rate_per_share)

print(f'Total Dividend: ${total_dividend:,.2f}')