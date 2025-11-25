import pymupdf


class PDFUtil:
    @classmethod
    async def get_pdf_text_content(cls, pdf_file: bytes) -> str:
        doc_text = []

        with pymupdf.open(stream=pdf_file, filetype="pdf") as pdf:
            for page in pdf:
                doc_text.append(page.get_text("text"))

        return "\n".join(doc_text)
