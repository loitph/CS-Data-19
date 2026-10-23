import os
import re
import pandas as pd
import numpy as np

excel_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logistics_ver2.xlsx")

if os.path.exists(excel_file):
  df = pd.read_excel(excel_file)
else:
  print(f'"{excel_file}" not found')

# skip the title row
df = df.iloc[1:]

# Tính Phí Vận Chuyện tại cột I
# Phí ban đầu (cost) = Cước cơ bản x Khối lượng (kg)
df["Phí vận chuyển (đ)"] = df["Khối lượng (kg)"] * df["Cước cơ bản (đ/kg)"]

# Theo khối lượng
# Weight <= 5kg (no discount)
# 5 < Weight <= 20kg (5% discount)
# Weight > 20kg (10% discount)
weight = df["Khối lượng (kg)"]
discount = np.select(
    [weight <= 5, weight <= 20],
    [1.0, 0.95],
    default=0.9,
)
df["Phí vận chuyển (đ)"] = df["Phí vận chuyển (đ)"] * discount

# Theo loại vận chuyển
# Loại vân chuyển "Siêu tốc" -> + 20_000 VND
type_of_delivery = df["Loại vận chuyển"]
df["Phí vận chuyển (đ)"] = np.where(
  type_of_delivery == "Siêu tốc",
  df["Phí vận chuyển (đ)"] + 20_000,
  df["Phí vận chuyển (đ)"]
)


# Giảm 5% nếu cùng miền
north_side = ["Hà Nội", "Hải Phòng", "Nam Định"]
mid_side = ["Đà Nẵng", "Huế"]
south_side = ["TP.HCM", "Cần Thơ", "Vũng Tàu"]

sender, receiver = df["Nơi gửi"], df["Nơi nhận"]

same_region = (
    (sender.isin(north_side) & receiver.isin(north_side))
    | (sender.isin(mid_side) & receiver.isin(mid_side))
    | (sender.isin(south_side) & receiver.isin(south_side))
)

df["Phí vận chuyển (đ)"] = np.where(same_region, df["Phí vận chuyển (đ)"] * 0.95, df["Phí vận chuyển (đ)"])


# Thêm cột "Phân loại cước"
# "Cao" > 500_000
# "Trung bình" 200_000 < Phí <= 500_000
# "Thấp" <= 200_000
fee = df["Phí vận chuyển (đ)"]
df["Phân loại cước"] = np.select(
    [fee > 500_000, fee > 200_000],
    ["Cao", "Trung bình"],
    default="Thấp",
)


# update the excel file
df.to_excel(excel_file, index=False)
print(f'Excel file "{excel_file}" updated successfully.')