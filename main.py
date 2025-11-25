import psycopg2
from openpyxl import Workbook
from config_database import REDSHIFT_CONFIG

def read_query_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

SQL_QUERY = read_query_file('query.sql')

from datetime import datetime, timedelta


def main():
    # List of dates to process
    date_list = [
        "2025-11-19",  '2025-11-20', '2025-11-21', '2025-11-24', '2025-11-25'  ]

    conn = psycopg2.connect(
        dbname=REDSHIFT_CONFIG["database"],
        user=REDSHIFT_CONFIG["user"],
        password=REDSHIFT_CONFIG["password"],
        host=REDSHIFT_CONFIG["host"],
        port=REDSHIFT_CONFIG["port"]
    )
    for date_str in date_list:
        with conn.cursor() as cur:
            cur.execute(SQL_QUERY, (date_str, date_str))
            if cur.description is not None:
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
            else:
                columns = []
                rows = []

            wb = Workbook()
            ws = wb.create_sheet(title="Results")
            wb.remove(wb["Sheet"])
            ws.append(list(columns))
            for row in rows:
                ws.append(list(row))
            filename = f"output_{date_str}.xlsx"
            wb.save(filename)
            print(f"Exported results to {filename}")

if __name__ == "__main__":
    main()
