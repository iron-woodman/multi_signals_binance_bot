import mysql.connector
from src.config_handler import TIMEFRAMES

def create_table(table_name):
  # Connect to the server using a context manager
  with mysql.connector.connect(
          host="localhost",
          user="bot",
          password="mybot123456",
          database="crypto_data"
  ) as cnx:
    # Create the table
    create_table_query = """
        CREATE TABLE IF NOT EXISTS {} (
            id INT auto_increment PRIMARY KEY,
            coin VARCHAR(50),
            date_time DATETIME,
            open_price DECIMAL(18, 8),
            high_price DECIMAL(18, 8),
            low_price DECIMAL(18, 8),
            close_price DECIMAL(18, 8),
            volume FLOAT
        )
        """.format(table_name)

    with cnx.cursor() as cursor:
      cursor.execute(create_table_query)

    cnx.commit()

def create_database(dbname):
  # Connect to the MySQL server
  cnx = mysql.connector.connect(
    host="localhost",
    user="bot",
    password="mybot123456"
  )
  # Create the database
  create_db_query = "CREATE DATABASE IF NOT EXISTS crypto_data"
  cursor = cnx.cursor()
  cursor.execute(create_db_query)


# Call the function to create the table
create_database("crypto_data")
for timeframe in TIMEFRAMES:
  create_table(f"spot_{timeframe}")
  create_table(f"fut_{timeframe}")

