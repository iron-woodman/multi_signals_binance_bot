import mysql.connector


def store_candle(candle_time, symbol, open_, high, low, close, volume, timeframe, is_spot=False):

    table_name = ''
    if is_spot:
        table_name = f'spot_{timeframe}'
    else:
        table_name = f'fut_{timeframe}'

    # Connect to the server using a context manager
    with mysql.connector.connect(
            host="localhost",
            user="bot",
            password="mybot",
            database="crypto_data"
    ) as cnx:
        insert_query =\
            f"INSERT INTO {table_name} (coin, date_time, open_price, high_price, low_price, close_price, volume) " \
            f"VALUES ('{symbol}', '{candle_time}', {open_}, {high}, {low}, {close}, {volume})"

        with cnx.cursor() as cursor:
            cursor.execute(insert_query)
            cnx.commit()

def get_candles(last_id, tablename):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="bot",
            password="mybot",
            database="crypto_data"
        )

        sql_select_Query = f"select * from {tablename} where id > {last_id}"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        # get all records
        records = cursor.fetchall()
        return records

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()



# def insert_data(table_name, data):
#     # Connect to the server using a context manager
#     with mysql.connector.connect(
#             host="localhost",
#             user="bot",
#             password="mybot",
#             database="crypto_data"
#     ) as cnx:
#         # Insert data into the table
#         insert_query = """
#         INSERT INTO {} (id, cryptocurrency, date_time, open_price, close_price, high_price, low_price, volume)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         """.format(table_name)
#
#         with cnx.cursor() as cursor:
#             for row in data:
#                 cursor.execute(insert_query, row)
#
#             cnx.commit()
#
#
# # Example usage:
# data = [
#     (1, 'Bitcoin', '2021-01-01 00:00:00', 29000.00, 30000.00, 30500.00, 28000.00, 1000.00),
#     (2, 'Ethereum', '2021-01-02 00:00:00', 1000.00, 1100.00, 1150.00, 950.00, 2000.00)
# ]
#
# insert_data('candlestick', data)