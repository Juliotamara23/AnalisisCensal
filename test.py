# test.py
import pandas as pd

ruta_archivo_viejo = 'Archivo/basededatosvieja.xlsx'
campos_importantes_viejo = ['FAMILIA', 'NUMERO DOCUMENTO', 'NOMBRE', 'APELLIDOS']

try:
    df_viejo_test = pd.read_excel(ruta_archivo_viejo, header=0)  # Especificamos que la fila 0 es el encabezado
    print(f"Lectura exitosa del archivo (forzando encabezado en la fila 0): {ruta_archivo_viejo}\n")
    print("Primeros 4 registros con los campos importantes:")
    if all(campo in df_viejo_test.columns for campo in campos_importantes_viejo):
        print(df_viejo_test[campos_importantes_viejo].head(4))
    else:
        print("¡Error! No se encontraron todas las columnas esperadas en el archivo.")
        print("Columnas encontradas:", df_viejo_test.columns.tolist())

except FileNotFoundError:
    print(f"¡Error! No se encontró el archivo en la ruta: {ruta_archivo_viejo}")
except Exception as e:
    print(f"Ocurrió un error al leer el archivo: {e}")