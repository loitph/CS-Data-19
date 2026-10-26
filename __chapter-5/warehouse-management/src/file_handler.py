import os
import pandas as pd
import json

def initial_warehouse():
  print("Empty! Please input!")
  warehouse = {}

  while True:
    try:

      # 1. Product name
      product_name = input("Enter the product's name (done to exit): ").strip()
      if (product_name.lower() == "done"):
        if len(warehouse) == 0:
          print("Warehouse must be not empty! Please input!")
          continue

        if not product_name:
          print("Product name cannot be empty. Please enter a name.")
          continue

        if product_name in warehouse:
          print("Product name already exists. Please enter a different name.")
          continue
        break

      # 2. Quantity
      quantity = int(input("Enter the quantity: "))
      if quantity <= 0:
        print("Quantity must be a positive number. Please enter a valid quantity.")
        continue

      # 3. Price
      price = float(input("Enter the price per unit (VND): "))
      if price <= 0:
        print("Price must be a positive number. Please enter a valid price.")
        continue

      # Add product to warehouse
      warehouse[product_name] = {"quantity": quantity, "price": price}
      print(f"{product_name} added successfully.")

      # Save warehouse to JSON file
    except ValueError:
      print("Invalid input. Please enter valid values for price and quantity.")
    except KeyError:
      print("Product name already exists. Please enter a different name.")
    except Exception as e:
      print(f"An error occurred: {str(e)}")

  print(f"Warehouse initialized with {len(warehouse)} products.")
  return warehouse

def load_data_from_json(filepath="data/warehouse.json"):
  if not os.path.exists(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    data_initial = initial_warehouse()

    with open(filepath, 'w', encoding='utf-8') as file:
      json.dump(data_initial, file, indent=2, ensure_ascii=False)
    print(f"Data saved to {filepath}")
    return data_initial

  try:
    with open(filepath, 'r', encoding='utf-8') as file:
      json.load()
  except Exception as e:
    print(f"Error {e}")
    return {}

def save_data_to_json(data, filepath="data/warehouse.json"):
  try:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as file:
      json.dump(data, file, indent=2, ensure_ascii=False)
    print(f"Data saved to {filepath}")
  except Exception as e:
    print(f"Error {e}")

def export_to_excel(data, filepath="data/warehouse.xlsx"):
  try:
    flat_list = []
    for product_name, info in data.items():
      flat_list.append({
        "product_name": product_name,
        "quantity": info["quantity"],
        "price": info["price"],
        "Total": info["quantity"] * info["price"]
      })
    df = pd.DataFrame(flat_list)
    df.to_excel(filepath, index=False)
    print(f"Data exported to {filepath}")
  except Exception as e:
    print(f"Error {e}") 