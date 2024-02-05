import os
import io
import codecs
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from .receipt import Receipt


def ocr_image(input_file, language, sharpen=False, timeout=20):
    """
    :param input_file: str
        Path to image to prettify
    :return: str
    """
    with Image.open(input_file) as img:
        img = img.filter(ImageFilter.SHARPEN)
        img = ImageEnhance.Contrast(img).enhance(2)
        img = ImageEnhance.Brightness(img).enhance(2)
        return pytesseract.image_to_string(img, lang="deu", timeout=20)


def _process_receipt(config, filename, out_dir=None, sharpen=False):
    result = ocr_image(filename, config.language, sharpen=sharpen)

    if out_dir:
        basename = os.path.basename(filename)
        if sharpen:
            basename += ".sharpen"
        out_filename = os.path.join(out_dir, basename + ".txt")
        with codecs.open(out_filename, "w") as fp:
            fp.write(result)
    else:
        out_filename = None

    return Receipt(config, out_filename or filename, result)


def process_receipt(config, filename, out_dir=None, verbosity=0):
    if filename.endswith(".txt"):
        if verbosity > 0:
            print("Parsing existing OCR result", filename)
        return Receipt.from_file(config, filename)

    if verbosity > 0:
        print("Performing scan on", filename)
    receipt = _process_receipt(config, filename, out_dir)

    if not receipt.is_complete():
        if verbosity > 0:
            print("Performing OCR scan with sharpening", filename)
        receipt2 = _process_receipt(config, filename, sharpen=True)
        receipt.merge(receipt2)

    return receipt
