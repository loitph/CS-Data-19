import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()

def run_upload_mysql():
    # Load environment variables
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = int(os.getenv('DB_PORT'))
    db_name = os.getenv('DB_NAME')

    database = db_name if db_name else 'company_db'

    try:
      # URL.create escapes special characters in the password; no database = server-level connection
      server_uri = URL.create("mysql+pymysql", username=db_user, password=db_password,
                              host=db_host, port=db_port)
      server_engine = create_engine(server_uri)

      with server_engine.connect() as connection:
        connection.execute(
          text(f"CREATE DATABASE IF NOT EXISTS `{database}`")
        )
        connection.commit()
      print(f"Database '{database}' created or already exists.")

      db_uri = server_uri.set(database=database)
      engine = create_engine(db_uri)

      csv_mapping = {
        "chart_of_accounts.csv": "chart_of_accounts",
        "customers.csv": "customers",
        "journal_q1.csv": "journal_q1",
        "journal_q2.csv": "journal_q2",
        "journal_q3.csv": "journal_q3",
        "journal_q4.csv": "journal_q4",
        "invoice_details.csv": "invoice_details",
        "payments.csv": "payments",
      }

      for csv_file, table_name in csv_mapping.items():
        path = os.path.join("dataraw", csv_file)
        if os.path.exists(path):
          df = pd.read_csv(path)
          df.to_sql(table_name, con=engine, if_exists='replace', index=False)
          print(f"Data from '{csv_file}' uploaded to table '{table_name} with {len(df)} rows'.")
        else:
          print(f"File '{csv_file}' not found in 'dataraw' directory.")
      print("Data upload to MySQL completed successfully.")

    except Exception as e:
      print(f"Error creating database: {e}")

if __name__ == "__main__":
    run_upload_mysql()