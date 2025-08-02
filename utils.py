import fitz  # PyMuPDF
import pandas as pd
from collections import defaultdict

ENGINE_CODES = ["ABM", "DT", "JU", "PP", "RN", "SA"]

def extract_page_with_part_number(file, part_number):
    """Find the page containing the part number in the PDF."""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    part_str = part_number.replace(" ", "")

    for i, page in enumerate(doc):
        text = page.get_text()
        if part_str in text.replace(" ", ""):
            return i, page
    return None, None

def extract_full_table_from_page(page):
    """Extracts all engine spec rows from a PDF page using visual layout grouping."""
    words = page.get_text("words")  # (x0, y0, x1, y1, word, block, line, word_no)

    # Group words by their Y position
    words_by_y = defaultdict(list)
    for w in words:
        x0, y0, x1, y1, word = w[:5]
        y_key = round(y0)
        words_by_y[y_key].append((x0, word))

    # Reconstruct lines sorted left-to-right
    grouped_rows = []
    for y in sorted(words_by_y.keys()):
        row = sorted(words_by_y[y], key=lambda x: x[0])
        text = " ".join(word for _, word in row)
        if text.startswith(tuple(ENGINE_CODES)):
            grouped_rows.append(text)

    # Parse rows into structured columns
    parsed_rows = []
    for row in grouped_rows:
        print(row)
        row = row.replace("→", " ").replace("(", "").replace(")", "")
        row = row.replace("cm³", "cm3").replace(",", ".")
        parts = row.split()

        if len(parts) >= 14:
            parsed_rows.append([
                parts[0],                 # Engine Code
                parts[1],                 # Production From
                parts[2],                 # Production To
                parts[3],                 # Fuel
                parts[4],                 # NA
                parts[5],                 # Cylinders
                f"{parts[6]} {parts[7]}", # Displacement
                parts[8],                 # Valves
                parts[9],                 # Power
                f"{parts[10]} {parts[11]}", # HP
                parts[12],                # CR
                parts[13]                 # Bore
            ])

    return pd.DataFrame(parsed_rows, columns=[
        "Engine Code", "Production From", "Production To", "Fuel", "NA",
        "Cyl", "Displacement", "Valves", "Power", "HP", "CR", "Bore"
    ]) if parsed_rows else pd.DataFrame()
