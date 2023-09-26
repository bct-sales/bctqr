from reportlab.graphics import shapes
from reportlab.lib import colors
from bctqr.images import load_charity_image, load_donation_image
from bctqr.qr import create_qr_code
import pydantic



class LabelData(pydantic.BaseModel):
    qr_data: str
    description: str
    price_in_cents: int
    charity: bool
    donation: bool
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
    font_size: int


class _LabelGenerator:
    __container: shapes.Drawing
    __label_size: tuple[float, float]
    __specs: SheetSpecifications
    __label_data: LabelData

    def __init__(self, *, container: shapes.Drawing, label_size: tuple[float, float], sheet_specifications: SheetSpecifications, label_data: LabelData):
        self.__container = container
        self.__label_size = label_size
        self.__label_data = label_data
        self.__specs = sheet_specifications

    def generate(self) -> None:
        self.__add_background()
        self.__add_qr_code()
        self.__add_description()
        self.__add_price()
        self.__add_charity()
        # self.__add_donation()

    def __add_background(self) -> None:
        label_width, label_height = self.__label_size
        self.__container.add(shapes.Rect(0, 0, label_width, label_height, fillColor=colors.red))

    def __add_qr_code(self) -> None:
        label_width, label_height = self.__label_size
        qr_data = self.__label_data.qr_data
        qr_image = create_qr_code(qr_data)
        self.__container.add(shapes.Image(0, 0, label_height, label_height, qr_image))

    def __add_description(self) -> None:
        label_width, label_height = self.__label_size
        description = self.__label_data.description
        font_size = self.__specs.font_size
        margin = self.__specs.margin
        self.__container.add(shapes.String(
            x=label_height + margin,
            y=label_height - font_size - margin,
            text=description,
            fontName="Helvetica",
            fontSize=font_size
        ))

    def __add_price(self) -> None:
        label_width, label_height = self.__label_size
        margin = self.__specs.margin
        font_size = self.__specs.font_size
        price_in_cents = self.__label_data.price_in_cents
        recipient_id = self.__label_data.recipient_id
        recipient_string = 'BCT' if recipient_id == 0 else f'#{recipient_id}'
        price_string = f"€{price_in_cents / 100:.2f} ➞ {recipient_string}"
        self.__container.add(shapes.String(
            x=label_height + margin,
            y=margin,
            text=price_string,
            fontName="Helvetica",
            fontSize=font_size
        ))

    def __add_charity(self) -> None:
        if self.__label_data.charity:
            label_width, label_height = self.__label_size
            image = load_charity_image()
            image_size = min(label_width * 0.1, label_height * 0.4)
            self.__container.add(shapes.Image(
                x=label_width - image_size,
                y=(label_height - image_size) / 2,
                width=image_size * 0.9,
                height=image_size * 0.9,
                path=image,
            ))

    def __add_donation(self) -> None:
        if self.__label_data.charity:
            label_width, label_height = self.__label_size
            image = load_donation_image()
            image_size = min(label_width * 0.1, label_height * 0.4)
            self.__container.add(shapes.Image(
                x=label_width - image_size,
                y=label_height - image_size,
                width=image_size * 0.9,
                height=image_size * 0.9,
                path=image,
            ))


def generate_label(*,
    container: shapes.Drawing,
    sheet_specifications: SheetSpecifications,
    label_data: LabelData,
    label_size: tuple[float, float]
):
    _LabelGenerator(
        container=container,
        label_size=label_size,
        sheet_specifications=sheet_specifications,
        label_data=label_data,
    ).generate()
