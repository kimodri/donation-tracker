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