from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
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
        dpi = 300

        # Convert A4 dimensions (210mm x 297 mm) to inches
        a4_width_mm, a4_height_mm = 210, 297
        mm_to_inch = 1 / 25.4
        width_inch = a4_width_mm * mm_to_inch
        height_inch = a4_height_mm * mm_to_inch

        # Calculate target size in pixels
        taget_width = int(width_inch * dpi)
        target_height = int(height_inch * dpi)

        # Resize the image to target dimensions (may stretch if aspect ratio differs)
        img_resized = img.resize((taget_width, target_height), Image.LANCZOS)

        # Create PDF vancas with A4 size (in points)
        pdf_canvas = canvas.Canvas(self.output_file_path, pagesize=A4)
        pdf_width, pdf_height = A4

        # Draw the resized image to fill the A4 page
        img_reader = ImageReader(img_resized)
        pdf_canvas.drawImage(img_reader, 0, 0, width=pdf_width, height=pdf_height)
        pdf_canvas.save()
