from typing import Optional
import pydantic


class LabelData(pydantic.BaseModel):
    qr_data: str
    description: str
    category: str
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
    label_width: float
    label_height: float
    corner_radius: int
    left_margin: Optional[float] = None
    right_margin: Optional[float] = None
    top_margin: Optional[float] = None
    bottom_margin: Optional[float] = None
    margin: int
    spacing: int
    font_size: int
    border: bool
