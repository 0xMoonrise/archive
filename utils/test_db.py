import psycopg2

db_params = {
    "host": "localhost",
    "dbname": "archive",
    "user": "postgresql",
    "password": "postgresql",
}

pdf_file_path = "tarea4.3.pdf"
filename = "tarea4.3.pdf"
conn = None

try:
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    with open(pdf_file_path, 'rb') as file:
        pdf_data = file.read()

    insert_query = """
    INSERT INTO pdf_schema.pdf_files (filename, data, editorial)
    VALUES (%s, %s, %s)
    """
    cur.execute(insert_query, (filename, psycopg2.Binary(pdf_data), "Tester"))
    conn.commit()

    print(f"[+] {filename} success!")

except Exception as e:
    print(f"Error: {e}")

finally:
    if conn:
        cur.close()
        conn.close()
