import mysql.connector


def create_table(table_name):
  # Connect to the server using a context manager
  with mysql.connector.connect(
          host="localhost",
          user="bot",
          password="mybot",
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
    password="mybot"
  )
  # Create the database
  create_db_query = "CREATE DATABASE IF NOT EXISTS crypto_data"
  cursor = cnx.cursor()
  cursor.execute(create_db_query)


# Call the function to create the table
create_database("crypto_data")
create_table("spot_5m")
create_table("fut_5m")
create_table("spot_4h")
create_table("fut_4h")

