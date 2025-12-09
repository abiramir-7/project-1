import pandas as pd
import psycopg2
import datetime

# Connect to your local DB
conn = psycopg2.connect(database="PROJECT-1", user="postgres", password="suga7", host="localhost")
cursor = conn.cursor()

# Read the provided CSV
df = pd.read_csv('env\\synthetic_client_queries.csv')

    # INSERT Logic
for index, row in df.iterrows():
    try:
        # Note: We pass 7 parameters. The last one is None because it's not closed yet.
        cursor.execute(
            """INSERT INTO queries 
               (client_email, client_mobile, query_heading, query_description, status, qdate_raised, date_closed) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (
                row['client_email'], 
                row['client_mobile'], 
                row['query_heading'], 
                row['query_description'], 
                'Open',           # Status is marked "Open" by default [cite: 59]
                datetime.now(),   # Raised time [cite: 58]
                None              # date_closed remains NULL 
            )
        )
    except Exception as e:
        print(f"Error at index {index}: {e}")
        break

conn.commit()
cursor.close()
conn.close()
print('Data imported Sucessfully')
