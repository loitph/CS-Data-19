from decimal import Decimal

name = input("Enter student name: ")
math_score = Decimal(input("Enter math score: "))
english_score = Decimal(input("Enter english score: "))
literature_score = Decimal(input("Enter literature score: "))

average_score = (math_score + english_score + literature_score) / 3

if average_score > 15:
  print(f"Passed!")
else:
  print(f"Failed!")