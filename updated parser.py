import pdfplumber

def extract_tables_with_page_info(file):
    tables = []

    with pdfplumber.open(file) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            table = page.extract_table()
            if table:
                tables.append({
                    "page": page_number,
                    "table": table
                })

    return tables
