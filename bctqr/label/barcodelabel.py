from reportlab.graphics import shapes
from reportlab.lib import colors
from bctqr.images import load_charity_image
from bctqr.barcode import generate_barcode
from bctqr.label.defs import LabelData, SheetSpecifications


class BarCodeLabelGenerator:
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
        # self.__add_background()
        self.__add_barcode()
        self.__add_description()
        self.__add_category()
        self.__add_item_id()
        self.__add_price_and_recipient()
        self.__add_charity()
        self.__add_border()

    def __add_barcode(self) -> None:
        label_width, label_height = self.__label_size
        margin = self.__specs.margin
        qr_data = self.__label_data.qr_data
        barcode = generate_barcode(data=qr_data, width=180)
        group = shapes.Group()
        group.add(barcode)
        group.shift(0, label_height - barcode.height - margin)
        self.__container.add(group)

    def __add_background(self) -> None:
        label_width, label_height = self.__label_size
        self.__container.add(shapes.Rect(0, 0, label_width, label_height, fillColor=colors.red))

    def __add_border(self) -> None:
        if self.__specs.border:
            label_width, label_height = self.__label_size
            self.__container.add(shapes.Rect(0, 0, label_width, label_height, fillColor=colors.transparent))

    def __add_description(self) -> None:
        label_width, label_height = self.__label_size
        description = self.__label_data.description
        font_size = self.__specs.font_size
        margin = self.__specs.margin
        spacing = self.__specs.spacing
        x = margin
        y = font_size * 3
        self.__container.add(shapes.String(
            x=x,
            y=y,
            text=description,
            fontName="Helvetica",
            fontSize=font_size
        ))

    def __add_category(self) -> None:
        label_width, label_height = self.__label_size
        category = self.__label_data.category
        font_size = self.__specs.font_size
        margin = self.__specs.margin
        spacing = self.__specs.spacing
        x = margin
        y = font_size * 2
        self.__container.add(shapes.String(
            x=x,
            y=y,
            text=category,
            fontName="Helvetica",
            fontSize=font_size
        ))

    def __add_price_and_recipient(self) -> None:
        label_width, label_height = self.__label_size
        margin = self.__specs.margin
        spacing = self.__specs.spacing
        font_size = self.__specs.font_size
        price_in_cents = self.__label_data.price_in_cents
        recipient_id = self.__label_data.recipient_id
        recipient_string = 'BCT' if recipient_id == 0 else f'#{recipient_id}'
        price_string = f"€{price_in_cents / 100:.2f} ➞ {recipient_string}"
        x = label_width - margin
        y = margin
        self.__container.add(shapes.String(
            x=x,
            y=y,
            text=price_string,
            fontName="Helvetica",
            fontSize=font_size,
            textAnchor='end',
        ))

    def __add_charity(self) -> None:
        if self.__label_data.charity:
            label_width, label_height = self.__label_size
            margin = self.__specs.margin
            image = load_charity_image()
            image_size = min(label_width * 0.1, label_height * 0.4)
            x = label_width - image_size - margin
            y = label_height - image_size - margin
            self.__container.add(shapes.Image(
                x=x,
                y=y,
                width=image_size,
                height=image_size,
                path=image,
            ))

    def __add_item_id(self) -> None:
        label_width, label_height = self.__label_size
        margin = self.__specs.margin
        font_size = self.__specs.font_size
        text = str(self.__label_data.item_id)
        x = margin
        y = margin
        self.__container.add(shapes.String(
            x=x,
            y=y,
            text=text,
            fontName="Helvetica",
            fontSize=font_size,
            textAnchor='start'
        ))