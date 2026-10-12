
scores = []

while True:
  score = float(input('Enter your score: '))
  scores.append(score)

  def calculate_average(score):
    if score >= 9.0:
        return print(f'{score} -> Excellent')
    elif 8.0 <= score < 9.0:
        return print(f'{score} -> Good')
    elif 6.5 <= score < 8.0:
        return print(f'{score} -> Fair')
    elif 5.0 <= score < 6.5:
        return print(f'{score} -> Average')
    else:
        return print(f'{score} -> Poor')

  for s in scores:
    calculate_average(s)

  if score < 0:
    print('Exiting...')
    print('Goodbye!')
    break