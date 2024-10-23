import psycopg2

DB_NAME = "temple_dev"
DB_USER = "webapp"
DB_PASS = "webapp"
DB_HOST = "localhost"
DB_PORT = "5432"



# Connect to your PostgreSQL database
# try:
#     conn = psycopg2.connect(database=DB_NAME,
#                             user=DB_USER,
#                             password=DB_PASS,
#                             host=DB_HOST,
#                             port=DB_PORT)
#     print("Database connected successfully")
# except psycopg2.Error as e:
#     print(f"Error connecting to database: {e}")
#     exit()

# # Open a cursor to perform database operations
# cur = conn.cursor()

# # Execute a query to fetch data from the 'user' table
# try:
#     cur.execute("SELECT * FROM user")  # Adjust the table name if needed
# except psycopg2.Error as e:
#     print(f"Error executing query: {e}")
#     conn.close()
#     exit()

# # Retrieve the query results (all rows)
# records = cur.fetchall()

# # Loop through the result and print each row (line item)
# for index, row in enumerate(records):
#     print(f"Line item {index + 1}: {row}",)

# # Close the cursor and connection after operations
# cur.close()
# conn.close()
# print("Database connection closed")

