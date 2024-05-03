import pdf2docx
import docx
import pandas as pd

def convert_pdf_to_word(pdf_path, output_path):
    pdf2docx.parse(pdf_path, output_path)

def extract_tables_from_docx(docx_path):
    doc = docx.Document(docx_path)
    tables = []
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                row_data.append(cell.text.strip())
            table_data.append(row_data)
        tables.append(pd.DataFrame(table_data))
    return tables

# PDF and Word file paths
pdf_path = r'C:\Users\mohan.7482\Desktop\PFRDA\Aggregaters PFRDA\Aggregators_PFRDA.pdf'
word_output_path = 'converted_word_document.docx'

# Convert PDF to Word
convert_pdf_to_word(pdf_path, word_output_path)

# Extract tables from Word
tables = extract_tables_from_docx(word_output_path)
# Concatenate tables into a single DataFrame
combined_df = pd.concat(tables, ignore_index=True)

# Save the combined DataFrame to an Excel file
excel_path = 'final_excel_sheet.xlsx'
combined_df.to_excel(excel_path, index=False)

print("Excel file has been created successfully.")