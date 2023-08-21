"""
PDF Handler Application

This application provider two main functionalites:

* Image to PDF Conventer: Converts an image file(jpg, jpeg, png, gif,bmp) into a PDF file.
* PDF Merger: Merges up to 4 PDF files into s single PDF file.

The application uses the PySimpleGUI library for the user interface and includes features to
select files and directiories, validate inputs, and perform the required operations.

Dependencies:
PySimpleGUI: GUI library for creating the user interface.
pathlib: Standard library module for handling file paths.
image_pdf_conventer: Custom module for converting image to PDF file
merge_pdf: Custom module for merging PDF files.

Usage:
Run this script to launch the PDF Handler application.
Application has two options: "IMAGE TO PDF CONVENTER" and "PDF MERGER"
For "IMAGE TO PDF CONVENTER" select an image file, provide an output directory
and specify a name for the PDF file.
For "PDF MERGER", select up to 4 PDF files, specify an output directory and provide name for merged PDF.

Note: This application id designed only for demonstration purposes.

Author: Cezary Tubacki
Date: August 2023
"""


import PySimpleGUI as sg
from image_pdf_conventer import ImagePdfConventer
from merge_pdf import PdfMerger
from pathlib import Path


def main():
    title_main = "PDF HANDLER"

    layout_main = [
        [sg.Button("IMAGE TO PDF CONVENTER")],
        [sg.Button("PDF MERGER")],
        [sg.Button("EXIT")],
    ]

    window_main = sg.Window(title_main, layout_main)

    while True:
        event, _ = window_main.read()
        if event in (sg.WIN_CLOSED, "EXIT"):
            break
        if event == "IMAGE TO PDF CONVENTER":
            title_convert = "IMAGE TO PDF CONVERTER"
            layout_convert = [
                [sg.Text("Chose your image file that you woud like to convert: ")],
                [sg.Button("SELECT IMAGE")],
                [sg.Text("", size=(60, 1), key="image_path")],
                [sg.Text("Chose your directory for conventered file: ")],
                [sg.InputText(key="pdf_path"), sg.FolderBrowse()],
                [sg.Text("Please enter a name for your pdf file")],
                [sg.Input(key="pdf_name")],
                [sg.Button("CONVERT"), sg.Button("BACK TO MENU")],
            ]
            window_convert = sg.Window(title_convert, layout_convert)

            while True:
                event_convert, values = window_convert.read()
                if event_convert in (sg.WIN_CLOSED, "BACK TO MENU"):
                    window_convert.close()
                    break
                if event_convert == "SELECT IMAGE":
                    image_path = sg.popup_get_file(
                        "Select an image", file_types=(("All Files", "*.*"),)
                    )
                    window_convert["image_path"].update(image_path)

                if event_convert == "CONVERT":
                    try:
                        # Validate image file:
                        if not validate_img_file(image_path):
                            sg.popup_error("Selected image file does not exist!")
                            window_convert["image_path"].update("")
                        # Validate output PDF directory:
                        elif not validate_output_pdfpath(values["pdf_path"]):
                            sg.popup_error("Please select a correct directory for PDF!")
                            window_convert["pdf_path"].update("")
                        # Validate PDF name:
                        if validate_name(values["pdf_name"]) is None:
                            sg.popup_error("Please enter a name for a pdf file!")
                            window_convert["pdf_name"].update("")

                        else:
                            # Make complete path for PDF file:
                            pdf_path = (
                                values["pdf_path"]
                                + "/"
                                + validate_name(values["pdf_name"])
                            )
                            # Convert an image to PDF:

                            image_to_convert = ImagePdfConventer(image_path, pdf_path)
                            image_to_convert.convert()
                            sg.popup("Done!")
                            window_convert.close()
                            break

                    except TypeError:
                        pass
                    except FileNotFoundError:
                        sg.popup_error("File not found!")
                    except UnboundLocalError:
                        sg.popup_error("Error occured during converting")

        if event == "PDF MERGER":
            title_merge = "PDF MERGER"
            layout_merge = [
                [sg.Button("SELECT PDF", key="pdf1")],
                [sg.Text("", size=(60, 1), key=1)],
                [sg.Button("SELECT PDF", key="pdf2")],
                [sg.Text("", size=(60, 1), key=2)],
                [sg.Button("SELECT PDF", key="pdf3")],
                [sg.Text("", size=(60, 1), key=3)],
                [sg.Button("SELECT PDF", key="pdf4")],
                [sg.Text("", size=(60, 1), key=4)],
                [sg.Text("Chose your directory for merged file: ")],
                [sg.InputText(key="merged_pdf_path"), sg.FolderBrowse()],
                [sg.Text("Please enter a name for your pdf file:")],
                [sg.Input(key="merged_pdf_name")],
                [sg.Button("MERGE"), sg.Button("BACK TO MENU")],
            ]

            window_merge = sg.Window(title_merge, layout_merge)
            pdf_path1 = ""
            pdf_path2 = ""
            pdf_path3 = ""
            pdf_path4 = ""

            while True:
                event_merge, values = window_merge.read()
                if event_merge in (sg.WIN_CLOSED, "BACK TO MENU"):
                    window_merge.close()
                    break
                if event_merge == "pdf1":
                    pdf_path1 = sg.popup_get_file(
                        "Select a pdf file",
                        file_types=(("PDF Files", "*.pdf"), ("All Files", "*.*")),
                    )
                    window_merge[1].update(pdf_path1)

                if event_merge == "pdf2":
                    pdf_path2 = sg.popup_get_file(
                        "Select a pdf file",
                        file_types=(("PDF Files", "*.pdf"), ("All Files", "*.*")),
                    )
                    window_merge[2].update(pdf_path2)

                if event_merge == "pdf3":
                    pdf_path3 = sg.popup_get_file(
                        "Select a pdf file",
                        file_types=(("PDF Files", "*.pdf"), ("All Files", "*.*")),
                    )
                    window_merge[3].update(pdf_path3)

                if event_merge == "pdf4":
                    pdf_path4 = sg.popup_get_file(
                        "Select a pdf file",
                        file_types=(("PDF Files", "*.pdf"), ("All Files", "*.*")),
                    )
                    window_merge[4].update(pdf_path4)

                if event_merge == "MERGE":
                    try:
                        pdf_paths = []

                        # Validate PDF files:
                        for i, path in enumerate(
                            [pdf_path1, pdf_path2, pdf_path3, pdf_path4], start=1
                        ):
                            if len(path) >= 1:
                                if not validate_pdf_file(path):
                                    sg.popup_error("Selected PDF file does not exist!")
                                    window_merge[i].update("")
                                else:
                                    pdf_paths.append(path)

                        # Check if there is at least 2 files in pdf_paths:
                        if len(pdf_paths) < 2:
                            sg.popup_error("At least 2 PDF file are required!")
                        # Validate PDF name:
                        elif validate_name(values["merged_pdf_name"]) is None:
                            sg.popup_error("Please enter a name for a merged PDF file!")
                            window_merge["merged_pdf_name"].update("")
                        # Validate PDF output path:
                        elif not validate_output_pdfpath(values["merged_pdf_path"]):
                            sg.popup_error("Please select a correct output PDF path!")
                            window_merge["merged_pdf_path"].update("")

                        else:
                            # Make merged PDF complete path:
                            merged_pdf_path = (
                                values["merged_pdf_path"]
                                + "/"
                                + validate_name(values["merged_pdf_name"])
                            )
                            # Instantiated an object of the class PdfMerger
                            make_pdf = PdfMerger(pdf_paths, merged_pdf_path)
                            # Merge PDF files
                            make_pdf.merge_pdf()
                            sg.popup("Done")
                            window_merge.close()
                            break

                    except TypeError:
                        pass
                    except FileNotFoundError:
                        sg.popup_error("File not found!")
                    except UnboundLocalError:
                        sg.popup_error("Error occurred during merging!")

    window_main.close()


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


if __name__ == "__main__":
    main()
