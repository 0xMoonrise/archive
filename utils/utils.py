import os

import re
from pdf2image import convert_from_path

pattern = re.compile(r'\.(md|pdf)$')


def is_valid_file_ext(string):
    return bool(pattern.search(string))


def get_image(file, from_path, to_path, page):
    if file.endswith('.pdf'):
        pdf_path = os.path.join(from_path, file)
        image_name = os.path.join(to_path, f"{os.path.splitext(file)[0]}.png")
        image = convert_from_path(pdf_path, first_page=page, last_page=page)
        if image:
            image[0].save(image_name, "PNG")
