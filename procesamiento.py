import pandas as pd

def procesar_datos(ruta_archivo):
    """
    Procesa un archivo XLSX para analizar familias, generar advertencias
    y detectar personas repetidas (basado en el campo 'Documento'),
    omitiendo personas con cédula '99'.

    Args:
        ruta_archivo (str): La ruta al archivo XLSX.

    Returns:
        tuple: Una tupla conteniendo:
            - dict: Familias con múltiples miembros.
            - dict: Familias con un solo miembro (jefe de familia solo).
            - list: Lista de advertencias encontradas (sin duplicados).
            - int: Total de personas procesadas (después de omitir '99').
            - pandas.DataFrame: DataFrame con información de personas repetidas (basado en 'Documento').
    """
    try:
        df = pd.read_excel(ruta_archivo)
        df.columns = df.columns.str.strip()
    except FileNotFoundError:
        return "Error: El archivo '{ruta_archivo}' no fue encontrado.", {}, {}, 0, pd.DataFrame()
    except Exception as e:
        return f"Error al leer el archivo '{ruta_archivo}': {e}", {}, {}, 0, pd.DataFrame()

    familias_multiples = {}
    familias_uno = {}
    advertencias = []
    total_personas = len(df)
    jefes_de_familia_documentos = set(df[df['Cedula de jefe(a) de Familia'].astype(str) == df['Documento'].astype(str)]['Documento'].astype(str).tolist())

    for jefe_cedula_num in df['Cedula de jefe(a) de Familia'].unique():
        jefe_cedula = str(jefe_cedula_num)
        familia = df[df['Cedula de jefe(a) de Familia'].astype(str) == jefe_cedula].copy()

        if not familia.empty:
            familia['Cedula de jefe(a) de Familia'] = familia['Cedula de jefe(a) de Familia'].astype(str)
            familia['Documento'] = familia['Documento'].astype(str)
            jefe_df = familia[familia['Cedula de jefe(a) de Familia'] == familia['Documento']].copy()

            if not jefe_df.empty:
                jefe_df['Nombre Completo Jefe'] = jefe_df['Primer Nombre'].astype(str).str.strip() + ' ' + \
                                                  jefe_df['Segundo Nombre'].fillna('').astype(str).str.strip() + ' ' + \
                                                  jefe_df['Primer Apellido'].astype(str).str.strip() + ' ' + \
                                                  jefe_df['Segundo Apellido'].fillna('').astype(str).str.strip()

                if len(jefe_df) == 1:
                    nombre_jefe = jefe_df.iloc[0]['Nombre Completo Jefe']
                    familia['Nombre Completo Miembro'] = familia['Primer Nombre'].astype(str).str.strip() + ' ' + \
                                                        familia['Segundo Nombre'].fillna('').astype(str).str.strip() + ' ' + \
                                                        familia['Primer Apellido'].astype(str).str.strip() + ' ' + \
                                                        familia['Segundo Apellido'].fillna('').astype(str).str.strip()
                    miembros_tabla = familia[['Documento', 'Nombre Completo Miembro']]
                    if len(miembros_tabla) > 1:
                        familias_multiples[jefe_cedula] = {"jefe": [jefe_df.iloc[0]['Documento'], nombre_jefe], "miembros": miembros_tabla}
                    else:
                        familias_uno[jefe_cedula] = {"jefe": [jefe_df.iloc[0]['Documento'], nombre_jefe], "miembros": miembros_tabla}

                elif len(jefe_df) > 1:
                    nombres_multiples_jefes = ", ".join(jefe_df['Primer Nombre'].astype(str).str.strip() + " " + jefe_df['Primer Apellido'].astype(str).str.strip())
                    advertencias.append([jefe_cedula, nombres_multiples_jefes, "Múltiples jefes de familia identificados con la misma cédula."])

    # Validar personas sin jefe de familia referenciado correctamente
    for index, row in df.iterrows():
        cedula_jefe = str(row['Cedula de jefe(a) de Familia'])
        documento_persona = str(row['Documento'])
        nombre_completo_persona = f"{str(row['Primer Nombre']).strip()} {str(row['Segundo Nombre']).strip() if pd.notna(row['Segundo Nombre']) else ''} {str(row['Primer Apellido']).strip()} {str(row['Segundo Apellido']).strip() if pd.notna(row['Segundo Apellido']) else ''}".strip()

        if cedula_jefe and cedula_jefe not in ['nan', 'None', ''] and cedula_jefe not in jefes_de_familia_documentos and cedula_jefe != documento_persona:
            advertencias.append([cedula_jefe, nombre_completo_persona, documento_persona])

    # Eliminar duplicados en las advertencias
    advertencias_unicas = []
    seen_warnings = set()
    for adv in advertencias:
        warning_tuple = tuple(adv)
        if warning_tuple not in seen_warnings:
            advertencias_unicas.append(adv)
            seen_warnings.add(warning_tuple)

    # Detectar personas repetidas (basado ÚNICAMENTE en 'Documento')
    conteo_documentos = df.groupby('Documento').size().reset_index(name='Cantidad')
    documentos_repetidos = conteo_documentos[conteo_documentos['Cantidad'] > 1]['Documento'].tolist()
    personas_repetidas_df = df[df['Documento'].isin(documentos_repetidos)].copy()

    if not personas_repetidas_df.empty:
        personas_repetidas_df['Nombre Completo Persona'] = personas_repetidas_df['Primer Nombre'].astype(str).str.strip() + ' ' + \
                                                          personas_repetidas_df['Segundo Nombre'].fillna('').astype(str).str.strip() + ' ' + \
                                                          personas_repetidas_df['Primer Apellido'].astype(str).str.strip() + ' ' + \
                                                          personas_repetidas_df['Segundo Apellido'].fillna('').astype(str).str.strip()
        # Agrupar por 'Documento' para obtener la información y la cantidad de repeticiones
        personas_repetidas_df = personas_repetidas_df.groupby(['Documento', 'Nombre Completo Persona', 'Cedula de jefe(a) de Familia']).size().reset_index(name='Cantidad')
        personas_repetidas_df.rename(columns={'Documento': 'Cedula Persona'}, inplace=True)
        personas_repetidas_df = personas_repetidas_df[['Cedula de jefe(a) de Familia', 'Nombre Completo Persona', 'Cedula Persona', 'Cantidad']]

    return familias_multiples, familias_uno, advertencias_unicas, total_personas, personas_repetidas_df