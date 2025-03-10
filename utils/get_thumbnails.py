import os
import sys
import psycopg2
from io import BytesIO
from pdf2image import convert_from_bytes

db_params = {
    "host": "localhost",
    "dbname": "archive",
    "user": "postgresql",
    "password": "postgresql",
}

conn = None

try:
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    get_no_thumbnails = "SELECT id, filename, data, cover_page FROM pdf_schema.pdf_files;"
    set_thumbnail = "UPDATE pdf_schema.pdf_files SET thumbnail_image = %s WHERE id = %s"
    cur.execute(get_no_thumbnails)

    for data in cur.fetchall():
        index, filename, file, cover_page = data

        img_byte_array = BytesIO()
        thumbnail = convert_from_bytes(BytesIO(file).read(),
                                       first_page=cover_page,
                                       last_page=cover_page)
        thumbnail[0].save(img_byte_array, format="WEBP", quality=100)
        webp_data = img_byte_array.getvalue()

        print(f"Thumbnail for {filename}: {len(webp_data)} bytes")
        
        try:
            cur.execute(set_thumbnail, (psycopg2.Binary(webp_data), index))
            conn.commit()
            print(f'{filename} has been successfully updated!')
        except Exception as e:
            print(f"Error updating thumbnail for {filename}: {e}")
            conn.rollback()

    print("[+] Success!")

except Exception as e:
    print(f"Error: {e}")

finally:
    if conn:
        cur.close()
        conn.close()
