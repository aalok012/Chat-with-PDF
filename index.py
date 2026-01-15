from pathlib import Path
pdf_path = Path(__file__).parent / "plato.pdf"

from langchain_community.document_loaders import PyPDFLoader
#load this file in python program
loader = PyPDFLoader(pdf_path)

docs= loader.load()