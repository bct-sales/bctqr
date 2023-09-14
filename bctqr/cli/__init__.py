import click
from reportlab.graphics import shapes
from bctqr.label import generate_label

from bctqr.qr import create_qr_code
import labels
import pydantic


@click.group()
def cli():
    pass


class LabelData(pydantic.BaseModel):
    qr_data: str
    description: str
    price_in_cents: int


class SheetData(pydantic.BaseModel):
    labels: list[LabelData]


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
@click.argument('output_file', type=click.Path(exists=False))
def generate(input_file: str, output_file: str):
    with open(input_file) as file:
        sheet_data: SheetData = SheetData.model_validate_json(file.read())

    specification = labels.Specification(210, 297, 2, 8, 90, 25, corner_radius=2)

    def create_label(label: shapes.Drawing, width: float, height: float, label_data: LabelData):
        generate_label(
            container=label,
            qr_data=label_data.qr_data,
            label_size=(width, height),
            caption=label_data.description,
            price_in_cents=label_data.price_in_cents,
        )

    sheet = labels.Sheet(
        specification,
        create_label
    )

    for label_data in sheet_data.labels:
        sheet.add_label(label_data)

    sheet.save(output_file)
