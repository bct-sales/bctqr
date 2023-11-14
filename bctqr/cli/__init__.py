import click
from reportlab.graphics import shapes
from bctqr.barcode import generate_barcode
from bctqr.images import load_charity_image
from bctqr.label import LabelData, SheetSpecifications, generate_label

import labels
import pydantic
import sys
from decimal import Decimal

@click.group()
def cli():
    pass


class SheetData(pydantic.BaseModel):
    labels: list[LabelData]
    sheet_specs: SheetSpecifications


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, allow_dash=True))
@click.argument('output_file', type=click.Path(exists=False))
def generate(input_file: str, output_file: str) -> int:
    if input_file == '-':
        raw_data = sys.stdin.read()
    else:
        with open(input_file) as file:
            raw_data = file.read()

    sheet_data = SheetData.model_validate_json(raw_data)
    sheet_specs = sheet_data.sheet_specs

    kwargs = {}
    for key in ["sheet_width", "sheet_height", "columns", "rows", "label_width", "label_height", "corner_radius", "left_margin", "right_margin", "top_margin", "bottom_margin"]:
        if value := getattr(sheet_specs, key):
            kwargs[key] = value
    specification = labels.Specification(**kwargs)

    def create_label(label: shapes.Drawing, width: float, height: float, label_data: LabelData):
        generate_label(
            container=label,
            label_size=(width, height),
            label_data=label_data,
            sheet_specifications=sheet_specs,
        )

    sheet = labels.Sheet(
        specification,
        create_label
    )

    for label_data in sheet_data.labels:
        sheet.add_label(label_data)

    sheet.save(output_file)
    return 0
