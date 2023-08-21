from PIL import Image
from reportlab.pdfgen import canvas
from dataclasses import dataclass

@dataclass
class ImagePdfConventer:
    """
    A class for converting an image file (jpg, jpeg, png, gif, bmp) into a PDF.

    Args:
        input_file_path (str): Path to the input image file.
        output_file_path (str): Path to the output PDF file.

    Attributes:
        input_file_path (str): Path to the input image file.
        output_file_path (str): Path to the output PDF file.

    Methods:
        convert(): Convert the input image to a PDF using reportlab.
    """

    __slots__ = ["input_file_path", "output_file_path"]

    input_file_path: str  # file path of input file (img, jpg, jpeg, png, bmp)
    output_file_path: str  # file of new pdf

    def convert(self):
        """
        Convert the input image to a PDF using reportlab.
        """
        img = Image.open(self.input_file_path)
        width, height = img.size

        c = canvas.Canvas(self.output_file_path, pagesize=(width, height))
        c.drawImage(self.input_file_path, 0, 0, width, height)
        c.save()
