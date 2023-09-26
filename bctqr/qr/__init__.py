from PIL import Image
import qrcode


def create_qr_code(data: str) -> Image:
    qr = qrcode.QRCode(
        box_size=2,
        border=4,
        error_correction=qrcode.ERROR_CORRECT_H,
    )

    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image()
