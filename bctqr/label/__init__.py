from reportlab.graphics import shapes
from reportlab.lib import colors
from bctqr.qr import create_qr_code



def generate_label(*,
    container: shapes.Drawing,
    qr_data: str,
    caption: str,
    price_in_cents: int,
    label_size: tuple[float, float]
):
    width, height = label_size
    qr_image = create_qr_code(qr_data)
    container.add(shapes.Rect(0, 0, width, height, fillColor=colors.red))
    container.add(shapes.Image(0, 0, height, height, qr_image))
    container.add(shapes.String(height + 10, height/2, caption, fontName="Helvetica", fontSize=14))

    price_string = f'€{price_in_cents / 100:.2f}'
    container.add(shapes.String(height + 10, height/4, price_string, fontName="Helvetica", fontSize=14))
