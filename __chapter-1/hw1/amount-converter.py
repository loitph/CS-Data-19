cents = int(input("Enter the amount in cents: "))
dollars = cents // 100
remaining_cents = cents % 100
print(f"${dollars}.{remaining_cents:02d}")