import pandas as pd

def formatear_datos(ruta_archivo_entrada, ruta_archivo_salida):
    """
    Lee un archivo XLSX, formatea los datos según los requerimientos
    y guarda el resultado en un nuevo archivo XLSX.

    Args:
        ruta_archivo_entrada (str): Ruta al archivo XLSX de entrada.
        ruta_archivo_salida (str): Ruta donde se guardará el nuevo archivo XLSX.
    """
    try:
        df = pd.read_excel(ruta_archivo_entrada)
        df.columns = df.columns.str.strip()
    except FileNotFoundError:
        return f"Error: El archivo '{ruta_archivo_entrada}' no fue encontrado."
    except Exception as e:
        return f"Error al leer el archivo '{ruta_archivo_entrada}': {e}"

    # Mantener la 'Cedula de jefe(a) de Familia' como la primera columna temporalmente
    df_formateado = df.copy()

    # Calcular el campo 'INTEGRANTES' (enumeración incremental por familia)
    df_formateado['INTEGRANTES'] = df_formateado.groupby('Cedula de jefe(a) de Familia').cumcount() + 1


    # Calcular el campo 'FAMILIA'
    familias_unicas = df['Cedula de jefe(a) de Familia'].unique()
    mapeo_familias = {cedula: i + 1 for i, cedula in enumerate(familias_unicas)}
    df_formateado['FAMILIA'] = df_formateado['Cedula de jefe(a) de Familia'].map(mapeo_familias)

    # Calcular el campo 'NUMERO DE VIVIENDA'
    familias_unicas = df['Cedula de jefe(a) de Familia'].unique()
    mapeo_viviendas = {cedula: i + 1 for i, cedula in enumerate(familias_unicas)}
    df_formateado['NUMERO DE VIVIENDA'] = df_formateado['Cedula de jefe(a) de Familia'].map(mapeo_viviendas)

    def formatear_nombres(nombre):
        """Formatea un nombre para que la primera letra de cada palabra sea mayúscula."""
        if isinstance(nombre, str):
            return ' '.join(palabra.capitalize() for palabra in nombre.lower().split())
        return nombre

    # Formatear las columnas de nombre
    columnas_nombre = ['Primer Nombre', 'Segundo Nombre', 'Primer Apellido', 'Segundo Apellido']
    for columna in columnas_nombre:
        if columna in df_formateado.columns:
            df_formateado[columna] = df_formateado[columna].apply(formatear_nombres)

    # Convertir el campo 'Parentesco' a minúsculas antes del mapeo
    df_formateado['PARENTESCO'] = df_formateado['Parentesco'].str.lower().str.strip().str.strip()
            
    # Mapeo para PARENTESCO
    mapeo_parentesco = {
        "Padre": "PA",
        "Madre": "MA",
        "Cónyuge": "CO",
        "Hermano(a)": "HE",
        "Cabeza de Familia": "CF",
        "Jefe de familia": "CF",
        "jefe de hogar": "CF",
        "Hermanastro(a)": "HE",
        "Esposo(a)": "ES",
        "Esposo": "ES",
        "Esposa": "ES",
        "Hijo(a)": "HI",
        "Hijastro": "HI",
        "Hijastra": "HI",
        "Yerno": "YR",
        "Nuera": "NU",
        "Suegro(a)": "SU",
        "Sobrino(a)": "SO",
        "Cuñado(a)": "CU",
        "Tío(a)": "TI",
        "Abuelo(a)": "AB",
        "Nieto": "NI",
        "Nieto(a)": "NI",
        "Nieta": "NI",
        "nietastro": "NI",
        "PRIMO": "PR",
        "PRIMA": "PR",
        "Prima": "PR",
        "Primo": "PR",
        "primo": "PR",
        "prima": "PR"
    }
    df_formateado['PARENTESCO'] = df_formateado['Parentesco'].map(mapeo_parentesco)

    # Mapeo para TIPO IDENTIFICACION
    mapeo_tipo_identificacion = {
        "Cédula de Ciudadanía": "CC",
        "Tarjeta de Identidad": "TI",
        "Registro Civil de Nacimiento": "RC",
        # Asumiendo que NUIP se maneja como RC, verificar si es diferente
        "Numero Único de Identificación Personal NUIP": "RC",
        "No tiene documento de identidad": "NI" # Asumiendo NI para "No tiene documento", verificar código correcto
    }
    df_formateado['TIPO IDENTIFICACION'] = df_formateado['Tipo de identificación'].map(mapeo_tipo_identificacion)

    # Mapeo para SEXO
    mapeo_sexo = {
        "Masculino": "M",
        "Femenino": "F"
    }
    df_formateado['SEXO'] = df_formateado['Sexo'].map(mapeo_sexo)

    # Mapeo para ESCOLARIDAD
    mapeo_escolaridad = {
        "Básica primaria (1° - 5°)": "PR",
        "Básica secundaria (6° - 9°)": "SE",
        "Media (10° - 13°)": "SE", # Asumiendo Media entra en Secundaria
        "Técnico": "UN", # Asumiendo Técnico entra en Universitaria, verificar si hay código específico
        "Tecnológico": "UN", # Asumiendo Tecnológico entra en Universitaria, verificar si hay código específico
        "Universitario": "UN",
        "Especialización": "UN", # Asumiendo Especialización entra en Universitaria
        "Maestría": "UN", # Asumiendo Maestría entra en Universitaria
        "Doctorado": "UN", # Asumiendo Doctorado entra en Universitaria
        "Ninguno": "NI",
        "NA": "NI" # Asumiendo NA como Ninguno
    }
    df_formateado['ESCOLARIDAD'] = df_formateado['Escolaridad'].map(mapeo_escolaridad)

    # Mapeo para ESTADO CIVIL
    mapeo_estado_civil = {
        "Soltero(a)": "S",
        "Casado(a)": "C",
        "Unión libre": "C", # Asumiendo Unión Libre como Casado, verificar si hay otro código
        "Divorciado(a)": "S", # Asumiendo Divorciado como Soltero, verificar si hay otro código
        "Viudo(a)": "S", # Asumiendo Viudo como Soltero, verificar si hay otro código
        "Separado": "S", # Asumiendo Separado como Soltero, verificar si hay otro código
        "No Informa": "S", # Asumiendo No Informa como Soltero, verificar si hay otro código
        "No Aplica": "S" # Asumiendo No Aplica como Soltero, verificar si hay otro código
    }
    df_formateado['ESTADO CIVIL'] = df_formateado['Estado civil'].map(mapeo_estado_civil)

    # Renombrar y seleccionar las columnas necesarias
    df_formateado = df_formateado.rename(columns={
        'Primer Nombre': 'PRIMER NOMBRE',
        'Segundo Nombre': 'SEGUNDO NOMBRE',
        'Primer Apellido': 'PRIMER APELLIDO',
        'Segundo Apellido': 'SEGUNDO APELLIDO',
        'Documento': 'NUMERO DOCUMENTO',
        'Fecha de nacimiento': 'FECHA NACIMIENTO',
        'Ocupación': 'OCUPACION',
        'Dirección': 'DIRECCION',
        'Teléfono': 'TELEFONO',
        'Hijos nacidos vivos': 'CANTIDAD DE HIJOS NACIDOS VIVOS',
        'Hijos sobrevivientes': 'NUMERO DE HIJOS SOBREVIVIENTES',
        'Fecha de nacimiento del último hijo nacido vivo': 'FECHA DE NACIMIENTO DEL ULTIMO HIJO NACIDO VIVO',
        'Personas fallecidas en el año anterior': 'CUANTAS PERSONAS FALLECIERON EL AÑO ANTERIOR',
        'Cedula de jefe(a) de Familia': 'CEDULA DE JEFE DE FAMILIA' # Renombrar la columna del jefe
    })

    # Formatear las columnas de fecha
    columnas_fecha = ['FECHA NACIMIENTO', 'FECHA DE NACIMIENTO DEL ULTIMO HIJO NACIDO VIVO']
    for columna in columnas_fecha:
        if columna in df_formateado.columns:
            try:
                df_formateado[columna] = pd.to_datetime(df_formateado[columna], errors='coerce').dt.strftime('%d/%m/%Y')
            except Exception as e:
                print(f"Error al formatear la columna '{columna}': {e}")

    # Seleccionar el orden de las columnas
    orden_columnas = [
        'CEDULA DE JEFE DE FAMILIA', # Ahora la columna renombrada del jefe
        'NUMERO DE VIVIENDA',
        'INTEGRANTES',
        'FAMILIA',
        'PRIMER NOMBRE',
        'SEGUNDO NOMBRE',
        'PRIMER APELLIDO',
        'SEGUNDO APELLIDO',
        'PARENTESCO',
        'TIPO IDENTIFICACION',
        'NUMERO DOCUMENTO',
        'SEXO',
        'FECHA NACIMIENTO',
        'ESCOLARIDAD',
        'OCUPACION',
        'ESTADO CIVIL',
        'DIRECCION',
        'TELEFONO',
        'CANTIDAD DE HIJOS NACIDOS VIVOS',
        'NUMERO DE HIJOS SOBREVIVIENTES',
        'FECHA DE NACIMIENTO DEL ULTIMO HIJO NACIDO VIVO',
        'CUANTAS PERSONAS FALLECIERON EL AÑO ANTERIOR'
    ]
    df_formateado = df_formateado[orden_columnas]

    # Guardar el nuevo archivo XLSX
    try:
        df_formateado.to_excel(ruta_archivo_salida, index=False)
        return f"Archivo formateado y guardado exitosamente en '{ruta_archivo_salida}'."
    except Exception as e:
        return f"Error al guardar el archivo formateado: {e}"

if __name__ == "__main__":
    ruta_archivo_entrada_xlsx = 'Archivo/Cuestionario Cabildo TATACHIO MIRABEL (Respuestas).xlsx'
    ruta_archivo_salida_xlsx = 'Archivo/datos_formateados.xlsx'
    resultado = formatear_datos(ruta_archivo_entrada_xlsx, ruta_archivo_salida_xlsx)
    print(resultado)