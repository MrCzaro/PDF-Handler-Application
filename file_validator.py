# file_validator
from pathlib import Path


class FileValidator:
    """
    Utility class for validating and handling file-related operations.

    This class provides static methods to validate image files,PDF files
    output PDF paths, and format PDF filenames.

    Usage:
        Use the static methods of this class to validate files and paths
        related to images and PDFs.
    """

    @staticmethod
    def validate_img_file(path):
        """
        Validate image file existence

        Args:
            path: str
        Returns:
            bool: True if the file is valid, False otherwise.
        """
        path = Path(path)
        return path.is_file() and path.suffix.lower() in [
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
        ]

    @staticmethod
    def validate_pdf_file(path):
        """
        Validate PDF existence

        Args:
            path: str
        Returns:
            bool: True if the file is valid, False otherwise.
        """
        path = Path(path)
        return path.is_file() and path.suffix.lower() == ".pdf"

    @staticmethod
    def validate_output_pdfpath(path):
        """
        Validate PDF output path

        Args:
            path (str): The output path.

        Returns:
            bool: True if the path is a valid directory, False otherwise.
        """
        path = Path(path)
        return path.is_dir()

    @staticmethod
    def validate_name(name):
        """
        Validate and format the provided PDF file.

        Args:
            name (str): The input filename.

        Returns:
            str: The validated and formatted PDF filename.
        """

        if not name:
            return None

        name = name.lower().strip()

        if not name.endswith(".pdf"):
            name += ".pdf"

        return name
