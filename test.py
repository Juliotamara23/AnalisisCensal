import csv
from fpdf import FPDF

with open("Archivo/Cuestionario Cabildo TATACHIO MIRABEL (Respuestas) - Respuestas de formulario 1.csv", encoding="utf8") as csv_file:
    data = list(csv.reader(csv_file, delimiter=","))

pdf = FPDF()
pdf.set_font("helvetica", size=14)

# Basic table:
pdf.add_page()
with pdf.table() as table:
    for data_row in data:
        row = table.row()
        for datum in data_row:
            row.cell(datum)

pdf.output("tuto5.pdf")