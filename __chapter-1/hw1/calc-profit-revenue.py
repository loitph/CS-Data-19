name_product_1 = input("Enter the name of the first product: ")
name_product_2 = input("Enter the name of the second product: ")

quantity_1 = int(input(f"Enter the quantity of {name_product_1}: "))
quantity_2 = int(input(f"Enter the quantity of {name_product_2}: "))

cost_price_1 = float(input(f"Enter the cost price of {name_product_1}: "))
cost_price_2 = float(input(f"Enter the cost price of {name_product_2}: "))

remaining_quantity_1 = int(input(f"Enter the remaining quantity of {name_product_1}: "))
remaining_quantity_2 = int(input(f"Enter the remaining quantity of {name_product_2}: "))

actual_total_revenue = (abs(quantity_1 - remaining_quantity_1) * cost_price_1) + (abs(quantity_2 - remaining_quantity_2) * cost_price_2)
print(f"Actual Total Revenue: ${actual_total_revenue:,.2f}")

expected_total_revenue = (quantity_1 * cost_price_1) + (quantity_2 * cost_price_2)
print(f"Expected Total Revenue: ${expected_total_revenue:,.2f}")


