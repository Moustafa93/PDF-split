import os
import typer
from typing_extensions import Annotated
from pdf2image import convert_from_path

def split(
        dirs:Annotated[list[str], typer.Argument(help="Directories of pdf files or folders. If a folder is given, split will process all pdfs in the folder.")], 
            ):
    cwd = os.getcwd()
    pdfs = []
    for dir in dirs:
        dir = os.path.join(cwd, dir)
        pdfs += handle_directory(dir)

    if not pdfs:
        print("No PDFs found")
        raise typer.Abort()
    
    print("Found the following PDFs:")
    for pdf in pdfs:
        print(pdf)
    confirmed = typer.confirm("Process all PDFs?")
    if not confirmed:
        print("PDFs not processed")
        raise typer.Abort()

    for pdf in pdfs:
        process_pdf(pdf)


def is_pdf(dir):
    return os.path.splitext(dir)[-1].lower() == ".pdf"


def is_directory(dir):
    return os.path.isdir(dir)

def handle_directory(dir):
    if is_pdf(dir):
        return [dir]
    pdf_dirs = []
    print(f"looking in directory {dir}...")
    for subdir in os.listdir(dir):
        full_path = os.path.join(dir,subdir)
        if is_directory(full_path):
            pdf_dirs += handle_directory(full_path)
        if is_pdf(full_path):
            pdf_dirs.append(full_path)
    return pdf_dirs

def process_pdf(input_dir, output_dir = ""):
    print(f"Processing pdf {input_dir} ...")
    if not output_dir:
        output_dir = input_dir.replace(".pdf", "")
    while os.path.exists(output_dir):
        output_dir += "(copy)"
    os.makedirs(output_dir)
    print(f"Saving to {output_dir}...")
    images_from_path = convert_from_path(input_dir, output_folder=output_dir, fmt="jpeg")
    print(f"Completed {input_dir}")