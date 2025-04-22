from fpdf import FPDF
from ..procesamiento import procesar_datos
import os
import pandas as pd

class PDFReport:
    def __init__(self, title: str):
        """
        Inicializa el reporte PDF con un título.
        :param title: Título para el documento PDF.
        """
        self.title = title
        self.pdf = FPDF(orientation='P', unit='mm', format='A3')
        # Unicode font
        self.pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf')
        self.pdf.add_font('DejaVu', 'B', 'fonts/DejaVuSans-Bold.ttf')
        self.pdf.set_font('DejaVu', size=10)

    def add_title(self):
        """Agrega el título al PDF."""
        self.pdf.add_page()
        self.pdf.set_font("DejaVu", style="B", size=16)
        self.pdf.cell(0, 10, self.title, new_x="LMARGIN", new_y="NEXT", align="C")
        self.pdf.ln(10)

    def sub_title(self):
        """Agrega un subtítulo al PDF."""
        self.pdf.add_page()
        self.pdf.set_font("DejaVu", style="B", size=14)
        self.pdf.cell(0, 10, self.title, new_x="LMARGIN", new_y="NEXT", align="C")
        self.pdf.ln(10)

    def add_description(self, text: str):
        """Agrega un texto descriptivo al PDF."""
        self.pdf.set_font("DejaVu", size=12)
        self.pdf.multi_cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.pdf.ln(5)

    def create_table_from_dataframe(self, df: pd.DataFrame):
        """Crea una tabla en el PDF a partir de un DataFrame de Pandas, centrada."""
        if df.empty:
            self.pdf.cell(0, 10, "No hay datos para mostrar en esta tabla.", new_x="LMARGIN", new_y="NEXT")
            return

        df_str = df.astype(str)
        COLUMNS = [list(df_str)]
        ROWS = df_str.values.tolist()
        DATA = COLUMNS + ROWS

        with self.pdf.table(
            borders_layout="MINIMAL",
            cell_fill_color=200,  # gris
            cell_fill_mode="ROWS",
            line_height=self.pdf.font_size * 2,
            text_align="CENTER",
            width=self.pdf.epw - 20, # Usa el ancho efectivo de la página menos un margen
            align='C' # Centra la tabla
        ) as table:
            for data_row in DATA:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)
        self.pdf.ln(5)

    def save_pdf(self, filename: str):
        """Genera el PDF y lo guarda en un archivo."""
        self.pdf.output(filename)

if __name__ == "__main__":
    ruta_archivo_xlsx = 'Archivo/Cuestionario Cabildo TATACHIO MIRABEL (Respuestas).xlsx'
    ruta_base_pdf = 'reportes/reportes_pdf'
    os.makedirs(ruta_base_pdf, exist_ok=True)
    nombre_archivo_familias_pdf = os.path.join(ruta_base_pdf, 'reporte_familias.pdf')
    nombre_archivo_un_miembro_pdf = os.path.join(ruta_base_pdf, 'reporte_1_miembro.pdf')
    nombre_archivo_advertencias_pdf = os.path.join(ruta_base_pdf, 'reporte_advertencias.pdf')
    nombre_archivo_repetidos_pdf = os.path.join(ruta_base_pdf, 'reporte_repetidos.pdf')

    resultado_analisis = procesar_datos(ruta_archivo_xlsx)

    if isinstance(resultado_analisis, str):
        print(resultado_analisis)
    else:
        familias_multiples, familias_uno, lista_advertencias, total_personas, personas_repetidas = resultado_analisis

        # Reporte de Familias Múltiples
        reporte_familias = PDFReport(title="REPORTE DE FAMILIAS CON VARIOS MIEMBROS REGISTRADOS")
        reporte_familias.add_title()
        reporte_familias.add_description(f"Este reporte detalla las familias con más de un miembro registrado en el sistema. Se encontraron {len(familias_multiples)} familias de un total de {total_personas} personas analizadas.")
        if familias_multiples:
            for jefe_cedula, data in familias_multiples.items():
                reporte_familias.pdf.cell(0, 10, "Jefe(a) de Familia:", new_x="LMARGIN", new_y="NEXT", align='C') # Updated ln
                jefe_df = pd.DataFrame([{"Documento": data['jefe'][0], "Nombre Completo": data['jefe'][1]}])
                reporte_familias.create_table_from_dataframe(jefe_df)
                reporte_familias.pdf.cell(0, 10, "Miembros de la Familia:", new_x="LMARGIN", new_y="NEXT", align='C') # Updated ln
                reporte_familias.create_table_from_dataframe(data['miembros'])
                reporte_familias.pdf.ln(5)
        else:
            reporte_familias.pdf.cell(0, 10, "No se encontraron familias con más de un miembro.", new_x="LMARGIN", new_y="NEXT", align='C') # Updated ln
        reporte_familias.save_pdf(nombre_archivo_familias_pdf)

        print("Reporte de familias con varios miembros en formato PDF generado exitosamente!")

        # Reporte de Jefes de Familia Solos
        reporte_un_miembro = PDFReport(title="REPORTE DE JEFES DE FAMILIA REGISTRADOS SIN OTROS MIEMBROS")
        reporte_un_miembro.add_title()
        reporte_un_miembro.add_description(f"Este reporte muestra a los jefes de familia que se registraron como el único miembro de su núcleo familiar. En total se encontraron {len(familias_uno)} jefes de familias registrados sin sus demas miembros de un total de {total_personas} personas analizadas.")
        reporte_un_miembro.add_description("Nota: Si usted es el único miembro de su familia, no es necesario registrar a otros miembros.")
        if familias_uno:
            jefes_solos_data = [{"Cédula del Jefe": data['jefe'][0], "Nombre del Jefe": data['jefe'][1]} for data in familias_uno.values()]
            jefes_solos_df = pd.DataFrame(jefes_solos_data)
            reporte_un_miembro.create_table_from_dataframe(jefes_solos_df)
        else:
            reporte_un_miembro.pdf.cell(0, 10, "No se encontraron jefes de familia registrados sin otros miembros.", new_x="LMARGIN", new_y="NEXT", align='C') # Updated ln
        reporte_un_miembro.save_pdf(nombre_archivo_un_miembro_pdf)

        print("Reporte de jefes de familia registrados sin otros miembros en formato PDF generado exitosamente!")

        # Reporte de Advertencias
        reporte_advertencias = PDFReport(title="REPORTE DE ADVERTENCIAS EN LOS REGISTROS DE FAMILIA")
        reporte_advertencias.add_title()
        reporte_advertencias.add_description(f"Este reporte detalla los posibles problemas encontrados en la información de los registros de familia. Se encontraron {len(lista_advertencias)} advertencias de un total de {total_personas} personas analizadas.")
        reporte_advertencias.add_description("No se encontró ningún jefe de familia asociado a los siguientes miembros registrados. Se recomienda revisar si la cédula del jefe de familia es incorrecta o si este aún no está registrado; (es obligatorio que este registrado).")
        if lista_advertencias:
            advertencias_df = pd.DataFrame(lista_advertencias, columns=["Cédula de Jefe de familia", "Nombre Completo (Persona)", "Cédula (Persona)"])
            reporte_advertencias.create_table_from_dataframe(advertencias_df)
        else:
            reporte_advertencias.pdf.cell(0, 10, "No se encontraron advertencias en los registros de familia.", new_x="LMARGIN", new_y="NEXT", align='C') # Updated ln
        reporte_advertencias.save_pdf(nombre_archivo_advertencias_pdf)

        print("Reporte de advertencia en formato PDF generado exitosamente!")

        # Reporte de Personas Repetidas
        reporte_repetidos = PDFReport(title="REPORTE DE PERSONAS REPETIDAS")
        reporte_repetidos.add_title()
        reporte_repetidos.add_description(f"Este reporte muestra las personas que aparecen más de una vez en el registro, identificadas por su número de documento. Se encontraron {len(personas_repetidas)} registros repetidos de un total de {total_personas} personas analizadas.")
        if not personas_repetidas.empty:
            reporte_repetidos.create_table_from_dataframe(personas_repetidas)
        else:
            reporte_repetidos.pdf.cell(0, 10, "No se encontraron personas repetidas en el registro.", new_x="LMARGIN", new_y="NEXT", align='C') # Updated ln
        reporte_repetidos.save_pdf(nombre_archivo_repetidos_pdf)

        print("Reporte de personas repetidas en formato PDF generado exitosamente!")