import click
from reportlab.graphics import shapes
from bctqr.images import load_charity_image
from bctqr.label import LabelData, SheetSpecifications, generate_label

import labels
import pydantic
import sys


@click.group()
def cli():
    pass


class SheetData(pydantic.BaseModel):
    labels: list[LabelData]
    sheet_specs: SheetSpecifications


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, allow_dash=True))
@click.argument('output_file', type=click.Path(exists=False))
def generate(input_file: str, output_file: str):
    if input_file == '-':
        raw_data = sys.stdin.read()
    else:
        with open(input_file) as file:
            raw_data = file.read()

    sheet_data = SheetData.model_validate_json(raw_data)
    specification = labels.Specification(**sheet_data.sheet_specs.model_dump())

    def create_label(label: shapes.Drawing, width: float, height: float, label_data: LabelData):
        generate_label(
            container=label,
            label_size=(width, height),
            label_data=label_data,
        )

    sheet = labels.Sheet(
        specification,
        create_label
    )

    for label_data in sheet_data.labels:
        sheet.add_label(label_data)

    sheet.save(output_file)


@cli.command()
def test():
    load_charity_image()
