import pandas as pd

def procesar_datos(ruta_archivo):
    """
    Procesa un archivo XLSX para analizar familias, generar advertencias
    y detectar personas repetidas (basado en 'Documento' y 'Nombre Completo'),
    omitiendo personas con cédula '99'.

    Args:
        ruta_archivo (str): La ruta al archivo XLSX.

    Returns:
        tuple: Una tupla conteniendo:
            - dict: Familias con múltiples miembros.
            - dict: Familias con un solo miembro (jefe de familia solo).
            - list: Lista de advertencias encontradas (sin duplicados).
            - int: Total de personas procesadas (después de omitir '99').
            - pandas.DataFrame: DataFrame con información de personas repetidas (basado en 'Documento' y 'Nombre Completo').
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

    df['Nombre Completo Persona'] = df['Primer Nombre'].astype(str).str.strip() + ' ' + \
                                      df['Segundo Nombre'].fillna('').astype(str).str.strip() + ' ' + \
                                      df['Primer Apellido'].astype(str).str.strip() + ' ' + \
                                      df['Segundo Apellido'].fillna('').astype(str).str.strip()

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
                    miembros_tabla = familia[['Documento', 'Nombre Completo Persona']]
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
        nombre_completo_persona = row['Nombre Completo Persona']

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

    # Detectar personas repetidas (basado en 'Documento' Y 'Nombre Completo Persona')
    conteo_repetidos = df.groupby(['Nombre Completo Persona', 'Documento']).size().reset_index(name='Cantidad')
    personas_repetidas_con_mismo_doc = conteo_repetidos[conteo_repetidos['Cantidad'] > 1]

    conteo_nombre_repetido_diff_doc = df.groupby('Nombre Completo Persona')['Documento'].nunique().reset_index(name='Cantidad_Docs')
    nombres_repetidos_diff_doc = conteo_nombre_repetido_diff_doc[conteo_nombre_repetido_diff_doc['Cantidad_Docs'] > 1]['Nombre Completo Persona'].tolist()
    personas_mismo_nombre_diff_doc_df = df[df['Nombre Completo Persona'].isin(nombres_repetidos_diff_doc)].copy()

    personas_repetidas_df = pd.concat([
        personas_repetidas_con_mismo_doc.rename(columns={'Documento': 'Cedula Persona'}),
        personas_mismo_nombre_diff_doc_df[['Cedula de jefe(a) de Familia', 'Nombre Completo Persona', 'Documento']].rename(columns={'Documento': 'Cedula Persona'})
    ], ignore_index=True)

    if not personas_repetidas_df.empty:
        # Agrupar para mostrar la cantidad de repeticiones por nombre completo (con diferentes documentos)
        nombre_repetido_counts = personas_repetidas_df.groupby('Nombre Completo Persona')['Cedula Persona'].nunique().reset_index(name='Cantidad_Docs_Repetido')
        personas_repetidas_df = pd.merge(personas_repetidas_df, nombre_repetido_counts, on='Nombre Completo Persona', how='left')
        personas_repetidas_df.rename(columns={'Cedula Persona': 'Cedula Persona'}, inplace=True)
        personas_repetidas_df = personas_repetidas_df[['Cedula de jefe(a) de Familia', 'Nombre Completo Persona', 'Cedula Persona', 'Cantidad_Docs_Repetido']].drop_duplicates(subset=['Nombre Completo Persona', 'Cedula Persona'])


    return familias_multiples, familias_uno, advertencias_unicas, total_personas, personas_repetidas_df