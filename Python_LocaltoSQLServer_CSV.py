import pandas as pd
import pyodbc

def import_data_from_csv_to_sql_server(csv_file_path, server, database, table):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Convert the 'Month' column to datetime format
    df['Month of Observation'] = pd.to_datetime(df['Month of Observation'])

    # Replace any NaN (Not a Number) values with None
    df = df.where(pd.notna(df), None)

    # Connect to SQL Server
    connection_string = f"Driver={{SQL Server}};Server={server};Database={database};Trusted_Connection=yes;"
    conn = pyodbc.connect(connection_string)

    # Drop the existing table if it exists
    drop_table_query = f"IF OBJECT_ID('{table}', 'U') IS NOT NULL DROP TABLE {table}"
    with conn.cursor() as cursor:
        cursor.execute(drop_table_query)
        conn.commit()

    # Create the new table with columns 'Month' and 'Median_Price'
    create_table_query = f"""
        CREATE TABLE {table} (
            [Month of Observation] DATE,
            [Median Home Price (NSA)] FLOAT
        )
    """
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
        conn.commit()

    # Convert DataFrame to a list of tuples (rows) to be inserted into the SQL Server table
    data_to_insert = [tuple(row) for row in df.itertuples(index=False)]

    # Prepare the SQL query for bulk insertion
    placeholders = ', '.join(['?' for _ in range(len(df.columns))])
    insert_query = f"INSERT INTO {table} VALUES ({placeholders})"

    # Execute the bulk insert operation
    with conn.cursor() as cursor:
        cursor.executemany(insert_query, data_to_insert)
        conn.commit()

    conn.close()

if __name__ == "__main__":
    csv_file_path = "C:\\Users\\eugen\\Downloads\\National.csv"
    server = "Eugene\SQLEXPRESS"
    database = "PowerBI_datawarehouse"
    table = "[National]"

    import_data_from_csv_to_sql_server(csv_file_path, server, database, table)

