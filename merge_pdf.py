import PyPDF2
from dataclasses import dataclass

@dataclass
class PdfMerger:
    """
    A class for merging multiple PDF files into a single PDF file.

    Args:
        input_pdf_files (list): List of input PDF file paths.
        output_pdf_file (str): Path to the output merged PDF file.

    Attributes:
        input_pdf_files (list): List of input PDF file paths.
        output_pdf_file (str): Path to the output merged PDF file.

    Methods:
    merge_pdf(): Merge the input PDF files into the output PDF file.
    """

    __slots__ = ["input_pdf_files", "output_pdf_file"]

    input_pdf_files: list
    output_pdf_file: str

    def merge_pdf(self):
        """
        Merge the input PDF files into the output PDF file.
        """

        merge = PyPDF2.PdfMerger()

        for pdf_file in self.input_pdf_files:
            merge.append(pdf_file)

        with open(self.output_pdf_file, "wb") as file:
            merge.write(file)
