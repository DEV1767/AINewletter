import tempfile
from pathlib import Path
import requests

from langchain_community.document_loaders import PyPDFLoader


def load_pdf(pdf_url: str):

    response = requests.get(pdf_url, timeout=30)
    response.raise_for_status()

    # Windows cannot re-open a still-open NamedTemporaryFile by path.
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = Path(temp_dir) / "paper.pdf"
        temp_file_path.write_bytes(response.content)

        loader = PyPDFLoader(str(temp_file_path))
        documents = loader.load()

    return documents