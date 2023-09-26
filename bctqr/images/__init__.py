import importlib.resources as resources
import PIL
from PIL.Image import Image


def load_charity_image() -> Image:
    return _load_image('charity.png')


def load_donation_image() -> Image:
    return _load_image('donation.png')


def _load_image(filename: str) -> Image:
    with resources.open_binary('bctqr.images', filename) as file:
        image = PIL.Image.open(file)
        image.load()
    return image
