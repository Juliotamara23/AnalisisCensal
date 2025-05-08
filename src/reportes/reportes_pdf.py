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
        self.pdf.set_font("DejaVu", style="B", size=18)
        self.pdf.cell(0, 10, self.title, new_x="LMARGIN", new_y="NEXT", align="C")
        self.pdf.ln(10)

    def sub_title(self):
        """Agrega un subtítulo al PDF."""
        self.pdf.add_page()
        self.pdf.set_font("DejaVu", style="B", size=14)
        self.pdf.cell(0, 10, self.title, new_x="LMARGIN", new_y="NEXT", align="C")
        self.pdf.ln(10)

    def add_description(self, text: str, link_text: str = None, link_url: str = None):
        """Agrega un texto descriptivo al PDF con soporte para enlaces con alias."""
        self.pdf.set_font("DejaVu", size=14)
        self.pdf.multi_cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.pdf.ln(1)

        if link_text and link_url:
            self.pdf.set_font("DejaVu", size=14)
            self.pdf.set_text_color(0, 0, 255)
            self.pdf.underline = True
            self.pdf.cell(0, 5, link_text, new_x="LMARGIN", new_y="NEXT", link=link_url)
            self.pdf.set_text_color(0, 0, 0)
            self.pdf.underline = False
            self.pdf.ln(5)
        elif text and not link_text and not link_url:
            self.pdf.ln(4)
        elif link_url and not link_text:
            self.pdf.set_font("DejaVu", size=10)
            self.pdf.set_text_color(0, 0, 100)
            self.pdf.cell(0, 5, link_url, new_x="LMARGIN", new_y="NEXT", link=link_url)
            self.pdf.set_text_color(0, 0, 0)
            self.pdf.ln(5)


    def create_table_from_dataframe(self, df: pd.DataFrame, col_widths=None):
        """Crea una tabla en el PDF a partir de un DataFrame de Pandas."""
        if df.empty:
            self.pdf.cell(0, 10, "No hay datos para mostrar en esta tabla.", new_x="LMARGIN", new_y="NEXT")
            return

        # Calcular el ancho de las columnas si no se proporciona
        if col_widths is None:
            col_widths = [self.pdf.epw / len(df.columns)] * len(df.columns)

        # Print headers
        self.pdf.set_font('DejaVu', 'B', 13)
        self.pdf.set_fill_color(200, 220, 255)  # Azul claro para encabezados

        for i, col in enumerate(df.columns):
            self.pdf.cell(col_widths[i], 7, str(col), border=1, align='C', fill=True)
        self.pdf.ln()

        # Print data rows
        self.pdf.set_font('DejaVu', '', 13)
        self.pdf.set_fill_color(255, 255, 255)  # Blanco para filas de datos

        for _, row in df.iterrows():
            for i, col in enumerate(df.columns):
                self.pdf.cell(col_widths[i], 6, str(row[col]), border=1, align='L')
            self.pdf.ln()

        self.pdf.ln(2)

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

        # Reporte de Familias Registradas
        reporte_familias = PDFReport(title="REPORTE DE FAMILIAS REGISTRADAS")
        reporte_familias.add_title()
        reporte_familias.add_description(
            f"Este reporte detalla las familias que se registraron por medio de la encuesta. Se encontraron {len(familias_multiples)} familias de un total de {total_personas} personas registradas.\n\n"
            "NOTA: Si usted no aparece en este reporte debera registrar a su familia por medio del siguiente formulario:",
            link_text="haciendo click aquí. (Es muy importante que lea bien lo que le preguntan en el formulario)",
            link_url="https://docs.google.com/forms/d/e/1FAIpQLScSEcH_fBTjVTwaQEKQVub78TnbFTwBLpWL-dbak4sc-ya5Ew/viewform?usp=sharing."
        )
        reporte_familias.add_description("Si usted y toda su familia aparecen registrados omita el mensaje anterior.")

        if familias_multiples:
            for jefe_cedula, data in familias_multiples.items():
                # Primero se muestra al jefe de familia
                nombre_completo = data['jefe'][1]   # Nombre completo del jefe
                documento = data['jefe'][0]         # Documento del jefe
                jefe_info = f"Jefe de Familia: {nombre_completo} ({documento})"
                # Configuramos la fuente y se muestra la información del jefe
                reporte_familias.pdf.set_font("DejaVu", style="B", size=13)
                reporte_familias.pdf.cell(0, 10, jefe_info, new_x="LMARGIN", new_y="NEXT", align='L')
                reporte_familias.pdf.cell(0, 10, "Miembros de la Familia:", new_x="LMARGIN", new_y="NEXT", align='C')
                reporte_familias.create_table_from_dataframe(data['miembros'])
                reporte_familias.pdf.ln(5)
        else:
            reporte_familias.pdf.cell(0, 10, "No se encontraron familias con más de un miembro.", new_x="LMARGIN", new_y="NEXT", align='C')
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
            reporte_un_miembro.pdf.cell(0, 10, "No se encontraron jefes de familia registrados sin otros miembros.", new_x="LMARGIN", new_y="NEXT", align='C')
        reporte_un_miembro.save_pdf(nombre_archivo_un_miembro_pdf)

        print("Reporte de jefes de familia registrados sin otros miembros en formato PDF generado exitosamente!")

        # Reporte de advertencias
        reporte_advertencias = PDFReport(title="REPORTE DE ADVERTENCIAS EN LOS REGISTROS DE FAMILIA")
        reporte_advertencias.add_title()
        reporte_advertencias.add_description(f"Este reporte detalla los posibles problemas encontrados en la información de los registros de familia. Se encontraron {len(lista_advertencias)} advertencias de un total de {total_personas} personas analizadas.")
        reporte_advertencias.add_description("No se encontró ningún jefe de familia asociado a los siguientes miembros registrados. Se recomienda revisar si la cédula del jefe de familia es incorrecta o si este aún no está registrado; (es obligatorio que este registrado).")
        if lista_advertencias:
            advertencias_df = pd.DataFrame(lista_advertencias, columns=["Cédula de Jefe de familia", "Nombre Completo (Persona)", "Cédula (Persona)"])
            reporte_advertencias.create_table_from_dataframe(advertencias_df)
        else:
            reporte_advertencias.pdf.cell(0, 10, "No se encontraron advertencias en los registros de familia.", new_x="LMARGIN", new_y="NEXT", align='C')
        reporte_advertencias.save_pdf(nombre_archivo_advertencias_pdf)

        print("Reporte de advertencia en formato PDF generado exitosamente!")

        # Reporte de personas repetidas
        reporte_repetidos = PDFReport(title="REPORTE DE PERSONAS REPETIDAS")
        reporte_repetidos.add_title()
        reporte_repetidos.add_description(f"Este reporte muestra las personas que aparecen más de una vez en el registro, identificadas por su número de documento. Se encontraron {len(personas_repetidas)} personas repetidas de un total de {total_personas} personas analizadas.")
        if not personas_repetidas.empty:
            reporte_repetidos.create_table_from_dataframe(personas_repetidas)
        else:
            reporte_repetidos.pdf.cell(0, 10, "No se encontraron personas repetidas en el registro.", new_x="LMARGIN", new_y="NEXT", align='C')
        reporte_repetidos.save_pdf(nombre_archivo_repetidos_pdf)

        print("Reporte de personas repetidas en formato PDF generado exitosamente!")