# reportes_avanzados.py
import pandas as pd
from fpdf import FPDF, XPos, YPos
import os

class PDFReportAvanzado(FPDF):
    def __init__(self, title):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.title = title
        self.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf')
        self.add_font('DejaVu', 'B', 'fonts/DejaVuSans-Bold.ttf')
        self.set_font('DejaVu', size=10)

    def header(self):
        self.set_font('DejaVu', 'B', 15)
        self.cell(0, 10, self.title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    def chapter_title(self, num, label):
        self.set_font('DejaVu', '', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, f'Capítulo {num}: {label}', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L', fill=1)
        self.ln(2)

    def chapter_body(self, text):
        self.set_font('DejaVu', '', 10)
        self.multi_cell(0, 5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def create_table_from_dataframe(self, df: pd.DataFrame, col_widths=None):
        if df.empty:
            self.cell(0, 10, "No hay datos para mostrar en esta tabla.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            return

        self.set_font('DejaVu', 'B', 10)
        cols = df.columns
        if col_widths is None:
            col_widths = [self.epw / len(cols)] * len(cols)

        for i, col in enumerate(cols):
            self.cell(col_widths[i], 7, col, border=1, align='C', fill=True)
        self.ln()
        self.set_font('DejaVu', '', 10)

        for index, row in df.iterrows():
            for i, col in enumerate(cols):
                self.cell(col_widths[i], 6, str(row[col]), border=1, align='L')
            self.ln()
        self.ln(2)

    def print_resumen(self, resumen):
        self.chapter_title(1, "Resumen General")
        if 'error' in resumen:
            self.chapter_body(resumen['error'])
            return
        self.chapter_body(f"Total de familias analizadas en la base de datos antigua: {resumen['total_familias_comparadas_vieja']}")
        self.chapter_body(f"Total de familias analizadas en la base de datos nueva: {resumen['total_familias_comparadas']}")
        self.chapter_body(f"Número total de personas en la base de datos antigua: {resumen['total_personas_vieja']}")
        self.chapter_body(f"Número total de personas en la nueva base de datos: {resumen['total_personas_nueva']}")
        self.chapter_body(f"Número total de personas faltantes de la base de datos antigua en la nueva: {resumen['total_personas_faltantes']}")
        self.ln(5)

    def print_reporte_familias(self, reporte_familias):
        self.chapter_title(2, "Detalle de Comparación por Familia Antigua (no se incluyen familias nuevas)")
        if 'error' in reporte_familias:
            self.chapter_body(reporte_familias['error'])
            return
        for familia_vieja, detalles in reporte_familias.items():
            self.set_font('DejaVu', 'B', 10)
            self.cell(0, 6, f"Familia Antigua (ID): {familia_vieja}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_font('DejaVu', '', 10)

            jefe_info = detalles.get('jefe_nueva_info')
            jefe_texto = f"Jefe de Familia (Nueva DB): {jefe_info['nombre']} ({jefe_info['documento']})" if jefe_info else "Jefe de Familia (Nueva DB): No identificado"
            self.cell(0, 6, jefe_texto, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            # Tabla de Miembros Presentes en la Base de Datos Antigua
            self.set_font('DejaVu', 'B', 10)
            self.cell(0, 6, "Miembros registrados en la base de datos antigua:", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
            self.set_font('DejaVu', '', 10)
            df_miembros_vieja = pd.DataFrame([{'Documento': doc.split('(')[-1][:-1], 'Nombre Completo': doc.split('(')[0].strip()} for doc in detalles['miembros_vieja']])
            self.create_table_from_dataframe(df_miembros_vieja, col_widths=[self.epw * 0.3, self.epw * 0.7])

            # Tabla de Miembros Encontrados en la Base de Datos Nueva
            self.set_font('DejaVu', 'B', 10)
            self.cell(0, 6, "Miembros encontrados en la nueva base de datos:", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
            self.set_font('DejaVu', '', 10)
            miembros_nueva_data = []
            for miembro in detalles['miembros_nueva']:
                nombre, parentesco_info = miembro.split(' - Parentesco: ')
                documento = nombre.split('(')[-1][:-1]
                nombre_completo = nombre.split('(')[0].strip()
                miembros_nueva_data.append({'Documento': documento, 'Nombre Completo': nombre_completo, 'Parentesco (Nueva DB)': parentesco_info})
            df_miembros_nueva = pd.DataFrame(miembros_nueva_data)
            self.create_table_from_dataframe(df_miembros_nueva, col_widths=[self.epw * 0.25, self.epw * 0.45, self.epw * 0.3])

            # Tabla de Miembros Faltantes
            if detalles['faltantes']:
                self.set_font('DejaVu', 'B', 10)
                self.cell(0, 6, "Miembros faltantes en la nueva base de datos:", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
                self.set_font('DejaVu', '', 10)
                faltantes_data = []
                for faltante in detalles['faltantes']:
                    nombre, parentesco_info = faltante.split(' - Parentesco (Nueva DB): ')
                    documento = nombre.split('(')[-1][:-1]
                    nombre_completo = nombre.split('(')[0].strip()
                    faltantes_data.append({'Documento': documento, 'Nombre Completo': nombre_completo, 'Parentesco (Nueva DB)': parentesco_info})
                df_faltantes = pd.DataFrame(faltantes_data)
                self.create_table_from_dataframe(df_faltantes, col_widths=[self.epw * 0.25, self.epw * 0.45, self.epw * 0.3])
            else:
                self.set_font('DejaVu', 'B', 10)
                self.cell(0, 6, "No hay miembros faltantes para esta familia.", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
                self.set_font('DejaVu', '', 10)
            self.ln(5)

    def print_advertencias_viejas_table(self, advertencias):
        if advertencias and 'error' not in advertencias:
            self.chapter_title(3, "Miembros de la DB Antigua sin Jefe de Familia Correspondiente en la Nueva DB")
            self.set_font('DejaVu', '', 10)
            df_advertencias = pd.DataFrame([{'Documento': a['Persona (Antigua)'].split('(')[-1][:-1], 'Nombre Completo': a['Persona (Antigua)'].split('(')[0].strip(), 'Familia Antigua (ID)': a['Familia Antigua (ID)'], 'Parentesco (Nueva DB)': a['Parentesco (Nueva DB)']} for a in advertencias])
            self.create_table_from_dataframe(df_advertencias, col_widths=[self.epw * 0.2, self.epw * 0.4, self.epw * 0.2, self.epw * 0.2])
            self.ln(5)
        elif 'error' in advertencias:
            self.chapter_body(advertencias['error'])

    def print_advertencias_viejas_table(self, advertencias):
        if advertencias and 'error' not in advertencias:
            self.chapter_title(3, "Miembros de la DB Antigua sin Jefe de Familia Correspondiente en la Nueva DB")
            self.set_font('DejaVu', '', 10)
            df_advertencias = pd.DataFrame([{'Documento': a['Persona (Antigua)'].split('(')[-1][:-1], 'Nombre Completo': a['Persona (Antigua)'].split('(')[0].strip(), 'Familia Antigua (ID)': a['Familia Antigua (ID)']} for a in advertencias])
            self.create_table_from_dataframe(df_advertencias, col_widths=[self.epw * 0.2, self.epw * 0.5, self.epw * 0.3])
            self.ln(5)
        elif 'error' in advertencias:
            self.chapter_body(advertencias['error'])

def comparar_bases_de_datos(ruta_vieja, ruta_nueva):
    try:
        df_vieja = pd.read_excel(ruta_vieja)
        df_nueva = pd.read_excel(ruta_nueva)

        df_nueva.columns = df_nueva.columns.str.strip()

        df_vieja = df_vieja[['FAMILIA', 'NUMERO DOCUMENTO', 'NOMBRE', 'APELLIDOS']].copy()
        df_vieja.columns = ['FAMILIA_VIEJA', 'DOCUMENTO_VIEJO', 'NOMBRE_VIEJA', 'APELLIDOS_VIEJA']
        df_vieja['DOCUMENTO_VIEJO'] = df_vieja['DOCUMENTO_VIEJO'].astype(str).str.strip()
        df_vieja['NOMBRE_COMPLETO_VIEJA'] = df_vieja['NOMBRE_VIEJA'].str.strip() + ' ' + df_vieja['APELLIDOS_VIEJA'].str.strip()
        df_vieja_doc_nombre = df_vieja.set_index('DOCUMENTO_VIEJO')['NOMBRE_COMPLETO_VIEJA'].to_dict()

        df_nueva = df_nueva[['Cedula de jefe(a) de Familia', 'Documento', 'Primer Nombre', 'Segundo Nombre', 'Primer Apellido', 'Segundo Apellido', 'Parentesco']].copy()
        df_nueva.columns = ['JEFE_FAMILIA_NUEVA', 'DOCUMENTO_NUEVO', 'NOMBRE_NUEVO_P', 'NOMBRE_NUEVO_S', 'APELLIDO_NUEVO_P', 'APELLIDO_NUEVO_S', 'PARENTESCO_NUEVO']
        df_nueva['DOCUMENTO_NUEVO'] = df_nueva['DOCUMENTO_NUEVO'].astype(str).str.strip()
        df_nueva['NOMBRE_COMPLETO_NUEVA'] = df_nueva[['NOMBRE_NUEVO_P', 'NOMBRE_NUEVO_S', 'APELLIDO_NUEVO_P', 'APELLIDO_NUEVO_S']].apply(lambda row: f"{row['NOMBRE_NUEVO_P']} {row['NOMBRE_NUEVO_S'] if pd.notna(row['NOMBRE_NUEVO_S']) else ''} {row['APELLIDO_NUEVO_P']} {row['APELLIDO_NUEVO_S'] if pd.notna(row['APELLIDO_NUEVO_S']) else ''}".strip(), axis=1)
        df_nueva_doc_nombre_completo = df_nueva.set_index('DOCUMENTO_NUEVO')['NOMBRE_COMPLETO_NUEVA'].to_dict()
        df_nueva_doc_parentesco = df_nueva.set_index('DOCUMENTO_NUEVO')['PARENTESCO_NUEVO'].to_dict()
        df_nueva_jefes_set = set(df_nueva['JEFE_FAMILIA_NUEVA'].astype(str).unique()) # Conjunto de cédulas de jefes de la nueva DB

        df_vieja_grouped = df_vieja.groupby('FAMILIA_VIEJA')['DOCUMENTO_VIEJO'].apply(list).to_dict()
        df_vieja_info = df_vieja.set_index('DOCUMENTO_VIEJO')['NOMBRE_COMPLETO_VIEJA'].to_dict()

        familias_comparadas_vieja = set(df_vieja_grouped.keys())
        familias_comparadas = set(df_nueva['JEFE_FAMILIA_NUEVA'].astype(str).unique()) # Ahora comparamos por los jefes únicos de la nueva DB
        personas_vieja_total = len(df_vieja)
        personas_nueva_total = len(df_nueva)
        personas_faltantes_total = 0
        lista_personas_faltantes = []
        reporte_por_familia = {}
        advertencias_viejas = []

        for familia_vieja, miembros_vieja_docs in df_vieja_grouped.items():
            jefe_familia_nueva_doc = None
            for doc_viejo in miembros_vieja_docs:
                if doc_viejo in df_nueva_jefes_set: # Verificamos si el documento antiguo es jefe en la nueva DB
                    jefe_familia_nueva_doc = doc_viejo
                    break

            miembros_nueva_docs = set()
            faltantes = []
            miembros_vieja_info_familia = {doc: df_vieja_info.get(doc) for doc in miembros_vieja_docs}
            jefe_nueva_info = {}

            if jefe_familia_nueva_doc:
                jefe_nueva_info['documento'] = jefe_familia_nueva_doc
                jefe_nueva_info['nombre'] = df_nueva_doc_nombre_completo.get(jefe_familia_nueva_doc, 'No encontrado')
                # Obtener los miembros de la nueva familia basados en el jefe encontrado
                nueva_familia_df = df_nueva[df_nueva['JEFE_FAMILIA_NUEVA'].astype(str) == jefe_familia_nueva_doc]
                miembros_nueva_docs = set(nueva_familia_df['DOCUMENTO_NUEVO'].astype(str).tolist())

                for doc_viejo in miembros_vieja_docs:
                    nombre_viejo = miembros_vieja_info_familia.get(doc_viejo, f"Nombre no encontrado (Doc: {doc_viejo})")
                    parentesco_nuevo = df_nueva_doc_parentesco.get(doc_viejo, 'No encontrado')
                    if doc_viejo not in miembros_nueva_docs:
                        faltantes.append(f"{nombre_viejo} ({doc_viejo}) - Parentesco (Nueva DB): {parentesco_nuevo}")
                        personas_faltantes_total = personas_vieja_total - personas_nueva_total
                        lista_personas_faltantes.append(f"{nombre_viejo} ({doc_viejo}) - Familia Antigua (ID): {familia_vieja} - Parentesco (Nueva DB): {parentesco_nuevo}")

                reporte_por_familia[familia_vieja] = {
                    'jefe_nueva_info': jefe_nueva_info,
                    'miembros_vieja': [f"{miembros_vieja_info_familia.get(doc, f'Nombre no encontrado (Doc: {doc})')} ({doc})" for doc in miembros_vieja_docs],
                    'miembros_nueva': [f"{df_nueva_doc_nombre_completo.get(doc, 'No encontrado')} ({doc}) - Parentesco: {df_nueva_doc_parentesco.get(doc, 'No encontrado')}" for doc in miembros_nueva_docs],
                    'faltantes': faltantes
                }
            else:
                for doc_viejo in miembros_vieja_docs:
                    nombre_viejo = miembros_vieja_info_familia.get(doc_viejo, f"Nombre no encontrado (Doc: {doc_viejo})")
                    parentesco_nuevo = df_nueva_doc_parentesco.get(doc_viejo, 'No encontrado')
                    advertencias_viejas.append({'Persona (Antigua)': f"{nombre_viejo} ({doc_viejo})", 'Familia Antigua (ID)': familia_vieja, 'Parentesco (Nueva DB)': parentesco_nuevo})

        return {
            'total_familias_comparadas_vieja': str(len(familias_comparadas_vieja)),
            'total_familias_comparadas': str(len(familias_comparadas)),
            'total_personas_vieja': str(personas_vieja_total),
            'total_personas_nueva': str(personas_nueva_total),
            'total_personas_faltantes': str(personas_faltantes_total),
            'reporte_por_familia': reporte_por_familia,
            'advertencias_viejas': advertencias_viejas
        }

    except FileNotFoundError as e:
        return {'error': f"Error: Archivo no encontrado: {e}"}
    except Exception as e:
        return {'error': f"Error al procesar los archivos: {e}"}

if __name__ == "__main__":
    ruta_archivo_viejo = 'Archivo/basededatosvieja.xlsx'
    ruta_archivo_nuevo = 'Archivo/Cuestionario Cabildo TATACHIO MIRABEL (Respuestas).xlsx'
    ruta_reporte_pdf = 'reportes/reportes_avanzados'
    nombre_reporte_pdf = os.path.join(ruta_reporte_pdf, 'reporte_avanzado.pdf')
    report_title = "REPORTE AVANZADO DE COMPARACIÓN DE BASES DE DATOS"

    os.makedirs(ruta_reporte_pdf, exist_ok=True)

    resultado_comparacion = comparar_bases_de_datos(ruta_archivo_viejo, ruta_archivo_nuevo)

    pdf = PDFReportAvanzado(report_title)
    pdf.add_page()
    pdf.print_resumen(resultado_comparacion)
    pdf.print_reporte_familias(resultado_comparacion.get('reporte_por_familia', {'error': 'No se generó el reporte por familia debido a un error previo.'}))
    pdf.print_advertencias_viejas_table(resultado_comparacion.get('advertencias_viejas', {'error': 'No se generaron las advertencias debido a un error previo.'}))
    pdf.output(nombre_reporte_pdf, 'F')

    print(f"Reporte avanzado generado exitosamente en: {nombre_reporte_pdf}")