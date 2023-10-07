from io import BytesIO
# from barcode import Code39, Code128
# from barcode.writer import ImageWriter
# from PIL import Image
from reportlab.graphics.barcode import createBarcodeDrawing


def generate_barcode(data: str, width: float):
    code = createBarcodeDrawing('Code128', value=data, width=150, height=30)
    return code


# def generate_barcode(data: str) -> Image.Image:
#     buffer = BytesIO()
#     writer = ImageWriter()
#     options = {
#         "module_height": 3,
#         "module_width": 0.2,
#         "font_size": 5,
#         "text_distance": 2,
#         # "background": "red",
#         "quiet_zone": 2.5,
#     }
#     Code128(data, writer=writer).write(buffer, options=options)
#     buffer.seek(0)
#     image = Image.open(buffer)
#     return trim_whitespace(image)


# def trim_whitespace(image: Image.Image) -> Image.Image:
#     # Don't touch left and right margins!
#     bw_pixels = list(image.convert('L').getdata())
#     top_margin = find_top_margin_height(bw_pixels, image.width)
#     bottom_margin = find_bottom_margin_height(bw_pixels, image.width)
#     return image.crop((0, top_margin, image.width, image.height - bottom_margin))


# def find_top_margin_height(pixels: list[int], image_width: int) -> int:
#     row = 0
#     while all(pixels[i] == 255 for i in range(row * image_width, (row + 1) * image_width)):
#         row += 1
#     return row


# def find_bottom_margin_height(pixels: list[int], image_width: int) -> int:
#     row = len(pixels) // image_width - 1
#     height = 0
#     while all(pixels[i] == 255 for i in range(row * image_width, (row + 1) * image_width)):
#         row -= 1
#         height += 1
#     return height
