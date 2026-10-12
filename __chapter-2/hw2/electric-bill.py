from decimal import Decimal

kWh = Decimal(input("Enter the number of kilowatt-hours (kWh) used: "))

while kWh < 0:
  print("Invalid input. Please enter a non-negative number.")
  kWh = Decimal(input("Enter the number of kilowatt-hours (kWh) used: "))

# 0 <= kWh <= 50 -> 1_800VND/kWh
# 51 <= kWh <= 100 -> 2_000VND/kWh
# 101 <= kWh <= 200 -> 2_500VND/kWh
# kWh > 200 -> 3_000VND/kWh

TIERS = [
  (Decimal(50), 1_800),
  (Decimal(100), 2_000),
  (Decimal(200), 2_500),
  (Decimal('Infinity'), 3_000),
]

total = Decimal(0)
prev_limit = Decimal(0)

for limit, rate in TIERS:
  if kWh <= prev_limit:
    break
  total += (min(kWh, limit) - prev_limit) * rate
  prev_limit = limit

print(f'Total: {total:,.2f} VND')