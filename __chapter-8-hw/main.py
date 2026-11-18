from src import (
  Action,
  analysis_high_low_numbers,
  analysis_numbers,
  analysis_prize_names,
  analysis_special_prize_by_month,
  build_datamarts,
  initial_data,
  run_menu,
)

ACTIONS: list[Action] = [
  ("Analysis of the rate of numbers", analysis_numbers),
  ("Prize names", analysis_prize_names),
  ("Special prizes by month", analysis_special_prize_by_month),
  ("High & low numbers", analysis_high_low_numbers),
]


def main() -> None:
  try:
    # initial data
    initial_data()
    build_datamarts()

    # run menu
    run_menu(ACTIONS)
  except Exception as e:  # noqa: BLE001
    print(e)


if __name__ == "__main__":
  main()
