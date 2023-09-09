from PIL import Image
import qrcode


def create_qr_code(data: str) -> Image:
    qr = qrcode.QRCode(
        box_size=2,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image()
