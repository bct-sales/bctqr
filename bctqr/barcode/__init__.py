from io import BytesIO
from barcode import Code39
from barcode.writer import ImageWriter
from PIL import Image


def generate_barcode(data: str) -> Image.Image:
    buffer = BytesIO()
    Code39(data, writer=ImageWriter()).write(buffer)
    buffer.seek(0)
    return Image.open(buffer)
