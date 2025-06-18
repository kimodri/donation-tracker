import sqlite3

db_file = r'C:\Users\KimSchool\Github Repos\donation-tracker\instance\db.sqlite'
def delete_all_table_contents(db_file):
    """
    Deletes the contents of all tables in an SQLite database.

    Args:
        db_file (str): The path to the SQLite database file.
    """
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Get a list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Iterate through tables and delete contents
        for table_name_tuple in tables:
            table_name = table_name_tuple[0]
            if table_name != 'sqlite_sequence': # Skip internal SQLite table if it exists
                print(f"Deleting contents from table: {table_name}")
                cursor.execute(f"DELETE FROM {table_name};")

        conn.commit()
        print("Contents of all tables deleted successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
delete_all_table_contents(db_file)

# # Example usage:
# db_filename = 'your_database.db' # Replace with your database file name
# # First, let's create a dummy database with some data for demonstration
# # In a real scenario, you would already have your database.
# try:
#     conn = sqlite3.connect(db_filename)
#     cursor = conn.cursor()
#     cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)''')
#     cursor.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, item TEXT)''')
#     cursor.execute("INSERT INTO users (name) VALUES ('Alice')")
#     cursor.execute("INSERT INTO users (name) VALUES ('Bob')")
#     cursor.execute("INSERT INTO products (item) VALUES ('Laptop')")
#     cursor.execute("INSERT INTO products (item) VALUES ('Mouse')")
#     conn.commit()
#     conn.close()
#     print(f"Dummy database '{db_filename}' created with some data.")
# except sqlite3.Error as e:
#     print(f"Error creating dummy database: {e}")

# # Now, call the function to delete the contents
# delete_all_table_contents(db_filename)

# # You can optionally verify by trying to select from a table
# try:
#     conn = sqlite3.connect(db_filename)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users;")
#     print("\nContents of 'users' table after deletion:", cursor.fetchall())
#     cursor.execute("SELECT * FROM products;")
#     print("Contents of 'products' table after deletion:", cursor.fetchall())
#     conn.close()
# except sqlite3.Error as e:
#     print(f"Error verifying contents: {e}")