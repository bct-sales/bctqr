from reportlab.graphics import shapes
from reportlab.lib import colors
from bctqr.images import load_charity_image, load_donation_image
from bctqr.label.qrlabel import QRLabelGenerator
from bctqr.qr import create_qr_code
import pydantic


class LabelData(pydantic.BaseModel):
    qr_data: str
    description: str
    price_in_cents: int
    charity: bool
    item_id: int
    owner_id: int
    recipient_id: int


class SheetSpecifications(pydantic.BaseModel):
    sheet_width: int
    sheet_height: int
    columns: int
    rows: int
    label_width: int
    label_height: int
    corner_radius: int
    margin: int
    spacing: int
    font_size: int
    border: bool


def generate_label(*,
    container: shapes.Drawing,
    sheet_specifications: SheetSpecifications,
    label_data: LabelData,
    label_size: tuple[float, float]
):
    QRLabelGenerator(
        container=container,
        label_size=label_size,
        sheet_specifications=sheet_specifications,
        label_data=label_data,
    ).generate()
