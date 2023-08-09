import requests
import pandas as pd
import pyodbc

def fetch_data_from_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute('''
        IF OBJECT_ID('Connecticut', 'U') IS NOT NULL
        DROP TABLE Connecticut;
    ''')
    cursor.execute('''
        CREATE TABLE Connecticut (
            [date] DATE,
            median_sale_price FLOAT
        );
    ''')
    connection.commit()
    print("Table created successfully.")

def insert_data_into_table(connection, data):
    df = pd.DataFrame(data)
    cursor = connection.cursor()
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO Connecticut ([date], median_sale_price)
            VALUES (?, ?);
        ''', row['date'], row['median_sale_price'])
    connection.commit()
    print("Data inserted successfully.")

def main():
    url = "https://data.ct.gov/resource/jpi8-zeza.json"
    connection_string = "DRIVER={SQL Server};SERVER=Eugene\SQLEXPRESS;DATABASE=PowerBI_datawarehouse;Trusted_Connection=yes;"

    try:
        data = fetch_data_from_json(url)
        connection = pyodbc.connect(connection_string)
        create_table(connection)
        insert_data_into_table(connection, data)
        connection.close()
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()