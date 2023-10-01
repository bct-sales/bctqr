from reportlab.graphics import shapes
from bctqr.label.barcodelabel import BarCodeLabelGenerator
from bctqr.label.defs import LabelData, SheetSpecifications
from bctqr.label.qrlabel import QRLabelGenerator



def generate_label(*,
    container: shapes.Drawing,
    sheet_specifications: SheetSpecifications,
    label_data: LabelData,
    label_size: tuple[float, float]
):
    # QRLabelGenerator(
    #     container=container,
    #     label_size=label_size,
    #     sheet_specifications=sheet_specifications,
    #     label_data=label_data,
    # ).generate()
    BarCodeLabelGenerator(
        container=container,
        label_size=label_size,
        sheet_specifications=sheet_specifications,
        label_data=label_data,
    ).generate()
