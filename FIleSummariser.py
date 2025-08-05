def read_file(path):
    try:
        if path.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        elif path.endswith(".pdf"):
            import PyPDF2
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                return "\n".join(p.extract_text() or "" for p in reader.pages)
        elif path.endswith(".docx"):
            import docx
            doc = docx.Document(path)
            return "\n".join(p.text for p in doc.paragraphs)
    except Exception:
        return None