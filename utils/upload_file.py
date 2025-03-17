import os
import sys
import psycopg2
from pdf2image import convert_from_bytes
from io import BytesIO

db_params = {
    "host": "localhost",
    "dbname": os.environ.get('DB_NAME', 'archive'),
    "user": os.environ.get('DB_USER', 'postgresql'),
    "password": os.environ.get('DB_PASS', 'postgresql'),
}

conn = None
path = '/opt/lectures/'
pdf_query = """
INSERT INTO archive_schema.archive (filename,
                                    file,
                                    editorial,
                                    cover_page,
                                    thumbnail_image)
VALUES (%s, %s, %s, %s, %s)
"""

md_query = """
INSERT INTO archive_schema.archive (filename, file, editorial)
VALUES (%s, %s, %s)
"""


try:
    for filename in os.listdir(path):
        pdf_file_path = os.path.join(path, filename)
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        with open(pdf_file_path, 'rb') as file:
            pdf_data = file.read()
        if 'pdf' in filename:
            print(f"[+] {filename} Starting conversion...")
            img_byte_array = BytesIO()

            thumbnail = convert_from_bytes(BytesIO(pdf_data).read(),
                                           first_page=1,
                                           last_page=1)

            thumbnail[0].save(img_byte_array, format="WEBP", quality=100)
            webp_data = img_byte_array.getvalue()

            print("[+] Conversion was successful!")          
            cur.execute(pdf_query,
                        (filename,
                        psycopg2.Binary(pdf_data),
                        "Default ED",
                        1,
                        psycopg2.Binary(webp_data))
            )

        else:
            cur.execute(md_query,
                        (filename,
                        psycopg2.Binary(pdf_data),
                        "Default ED"))
        conn.commit()

        print(f"[+] {filename} success!")
except Exception as e:
    print(f"Error: {e}")

finally:
    if conn:
        cur.close()
        conn.close()
