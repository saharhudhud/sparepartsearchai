import fitz  # PyMuPDF
import pandas as pd

def extract_page_with_part_number(file, part_number):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    part_str = part_number.replace(" ", "")
    
    for i, page in enumerate(doc):
        page_text = page.get_text()
        if part_str in page_text.replace(" ", ""):
            return i, page.get_text("blocks")  # return matching page and blocks
    return None, None

def extract_structured_table_from_blocks(blocks):
    rows = []
    for block in blocks:
        text = block[4].strip()
        if any(code in text for code in ["ABM", "DT", "JU", "PP", "RN", "SA"]):  # unique row identifiers
            parts = text.split()
            if len(parts) >= 10:
                rows.append(parts[:11])  # capture standard row length
    return pd.DataFrame(rows, columns=[
        "Engine Code", "Production", "Fuel", "NA", "Cyl", "Displacement",
        "Valves", "Power", "HP", "CR", "Bore"
    ])
