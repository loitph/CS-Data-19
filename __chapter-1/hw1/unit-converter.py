# 1 galleon = 17 sickles
# 1 sickle = 29 knuts
knuts = int(input("Enter the amount in knuts: "))
galleons = knuts // (17 * 29)
remaining_knuts = knuts % (17 * 29)
sickles = remaining_knuts // 29
remaining_knuts = remaining_knuts % 29
print(f"{galleons} galleons, {sickles} sickles, {remaining_knuts} knuts")