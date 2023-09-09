import click
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader

from bctqr.qr import create_qr_code


@click.command()
def cli():
    qr_image = create_qr_code('test')
    canvas = Canvas("hello.pdf")
    canvas.drawImage(ImageReader(qr_image.get_image()), 100, 100, width=200, height=200)
    canvas.showPage()
    canvas.save()
