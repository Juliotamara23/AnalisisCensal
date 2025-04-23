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

    # Calcular el campo 'INTEGRANTES' (conteo total por familia - método viejo)
    # conteo_integrantes = df.groupby('Cedula de jefe(a) de Familia').size().to_dict()
    # df_formateado['INTEGRANTES'] = df_formateado['Cedula de jefe(a) de Familia'].map(conteo_integrantes)

    # Calcular el campo 'INTEGRANTES' (enumeración incremental por familia - nuevo método)
    df_formateado['INTEGRANTES'] = df_formateado.groupby('Cedula de jefe(a) de Familia').cumcount() + 1

    # Calcular el campo 'FAMILIA'
    familias_unicas = df['Cedula de jefe(a) de Familia'].unique()
    mapeo_familias = {cedula: i + 1 for i, cedula in enumerate(familias_unicas)}
    df_formateado['FAMILIA'] = df_formateado['Cedula de jefe(a) de Familia'].map(mapeo_familias)

    # Renombrar y seleccionar las columnas necesarias
    df_formateado = df_formateado.rename(columns={
        'Primer Nombre': 'PRIMER NOMBRE',
        'Segundo Nombre': 'SEGUNDO NOMBRE',
        'Primer Apellido': 'PRIMER APELLIDO',
        'Segundo Apellido': 'SEGUNDO APELLIDO',
        'Parentesco': 'PARENTESCO',
        'Tipo de identificación': 'TIPO IDENTIFICACION',
        'Documento': 'NUMERO DOCUMENTO',
        'Sexo': 'SEXO',
        'Fecha de nacimiento': 'FECHA NACIMIENTO',
        'Escolaridad': 'ESCOLARIDAD',
        'Ocupación': 'OCUPACION',
        'Estado civil': 'ESTADO CIVIL',
        'Dirección': 'DIRECCION',
        'Teléfono': 'TELEFONO',
        'Hijos nacidos vivos': 'CANTIDAD DE HIJOS NACIDOS VIVOS',
        'Hijos sobrevivientes': 'NUMERO DE HIJOS SOBREVIVIENTES',
        'Fecha de nacimiento del último hijo nacido vivo': 'FECHA DE NACIMIENTO DEL ULTIMO HIJO NACIDO VIVO',
        'Personas fallecidas en el año anterior': 'CUANTAS PERSONAS FALLECIERON EL AÑO ANTERIOR'
    })

    # Formatear las columnas de fecha
    columnas_fecha = ['FECHA NACIMIENTO', 'FECHA DE NACIMIENTO DEL ULTIMO HIJO NACIDO VIVO']
    for columna in columnas_fecha:
        if columna in df_formateado.columns:
            # Intentar convertir a datetime, manejar posibles errores
            try:
                df_formateado[columna] = pd.to_datetime(df_formateado[columna], errors='coerce').dt.strftime('%d/%m/%Y')
            except Exception as e:
                print(f"Error al formatear la columna '{columna}': {e}")
                # Si hay un error, se mantiene el formato original

    # Seleccionar el orden de las columnas
    orden_columnas = [
        'Cedula de jefe(a) de Familia', # Se mantiene como la primera columna temporalmente
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