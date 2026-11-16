import src


def main():
  print("Initializing the data mart processing...")

  src.run_upload_mysql()

  src.run_process_mart()
  print("Data mart processing completed successfully.")

if __name__ == "__main__":
  main()