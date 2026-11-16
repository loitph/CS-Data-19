import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()

def run_process_mart():
  print("Starting data processing for the data mart...")
  db_user = os.getenv('DB_USER')
  db_password = os.getenv('DB_PASSWORD')
  db_host = os.getenv('DB_HOST')
  db_port = int(os.getenv('DB_PORT'))
  db_name = os.getenv('DB_NAME')

  database = db_name if db_name else 'company_db'

  try:
    server_uri = URL.create("mysql+pymysql", username=db_user, password=db_password,
                            host=db_host, port=db_port)
    db_uri = server_uri.set(database=database)
    engine = create_engine(db_uri)

    df_accounts = pd.read_sql("SELECT * FROM chart_of_accounts", con=engine)
    df_customers = pd.read_sql("SELECT * FROM customers", con=engine)
    df_journal_q1 = pd.read_sql("SELECT * FROM journal_q1", con=engine)
    df_journal_q2 = pd.read_sql("SELECT * FROM journal_q2", con=engine)
    df_journal_q3 = pd.read_sql("SELECT * FROM journal_q3", con=engine)
    df_journal_q4 = pd.read_sql("SELECT * FROM journal_q4", con=engine)

    df_journal = pd.concat([df_journal_q1, df_journal_q2, df_journal_q3, df_journal_q4], ignore_index=True)
    df_journal = df_journal.sort_values(by=['account', 'date']).reset_index(drop=True)
    df_journal['previous_balance'] = df_journal['amount'].shift(1)
    df_journal['amount_diff'] = df_journal['amount'] - df_journal['previous_balance']

    master_df = pd.merge(df_journal, df_accounts, on='account_id', how='left')
    
    

  except Exception as e:
    print(f"Error connecting to the database: {e}")
    return