from tabulate import tabulate
from ..procesamiento import procesar_datos

def generar_reporte_familias_txt(familias, nombre_archivo, total_personas):
    num_familias = len(familias)
    total_miembros = 0
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write("=" * 20 + " FAMILIAS CON MAS DE 1 MIEMBRO REGISTRADO " + "=" * 20 + "\n\n")
        archivo.write("Esta tabla muestra a las familias por jefe de las mismas\n")
        archivo.write(f"\nSe encontraron {num_familias} familias con más de 1 miembro registrado de un total de {total_personas} personas.\n")
        for jefe_cedula, data in familias.items():
            archivo.write(f"\n{'=' * 30} Familia con Cédula de Jefe(a) de Familia: {jefe_cedula} {'=' * 30}\n")
            archivo.write("\nMiembros de la Familia:\n")
            archivo.write(tabulate(data['miembros'], headers='keys', tablefmt='grid', showindex=False) + "\n")
            total_miembros += len(data['miembros']) + 1 # +1 para el jefe
    print(f"El reporte de familias con más de 1 miembro ha sido guardado en '{nombre_archivo}'.")

def generar_reporte_un_miembro_txt(familias, nombre_archivo, total_personas):
    num_jefes_solos = len(familias)
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write("=" * 20 + " JEFES DE FAMILIA REGISTRADOS SIN OTROS MIEMBROS " + "=" * 20 + "\n\n")
        archivo.write("Esta tabla muestra a los jefes de familia que se registraron como el único miembro de su núcleo familiar.\nEsto podría indicar que faltan miembros por registrar o que realmente son familias unipersonales.\n\n")
        tabla_jefes_solos = [["Cédula del Jefe", "Nombre del Jefe"]]
        for jefe_cedula, data in familias.items():
            jefe_doc, jefe_nombre = data['jefe']
            tabla_jefes_solos.append([jefe_doc, jefe_nombre])
        archivo.write(tabulate(tabla_jefes_solos, headers="firstrow", tablefmt="grid"))
        archivo.write(f"\n\nSe encontraron {num_jefes_solos} jefes de familia registrados sin otros miembros de un total de {total_personas} personas en el registro.\n")
    print(f"El reporte de jefes de familia registrados sin otros miembros ha sido guardado en '{nombre_archivo}'.")

def generar_reporte_advertencias_txt(advertencias, nombre_archivo, total_personas):
    num_advertencias = len(advertencias)
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write("=" * 20 + " REPORTE DE ADVERTENCIAS EN LOS REGISTROS DE FAMILIA " + "=" * 20 + "\n\n")
        archivo.write("No se encontró ningún jefe de familia asociado a estas persona. Se recomienda revisar la cédula del jefe de familia.\n\n")
        archivo.write(f"Se encontraron {num_advertencias} personas con advertencias de un total de {total_personas} personas en el registro.\n")
        if advertencias:
            tabla_advertencias = [["Cédula de Jefe de familia", "Nombre Completo (Persona)", "Cédula (Persona)", "Mensaje"]]
            tabla_advertencias.extend([[str(adv[0]), adv[1], str(adv[2])] for adv in advertencias])
            archivo.write(tabulate(tabla_advertencias, headers="firstrow", tablefmt="grid"))
            print(f"El reporte de advertencias ha sido guardado en '{nombre_archivo}'.")
        else:
            archivo.write("No se encontraron advertencias en los registros de familia.\n")
            print(f"No se encontraron advertencias. El archivo '{nombre_archivo}' ha sido creado.")

def generar_reporte_repetidos_txt(repetidos_df, nombre_archivo, total_personas):
    num_repetidos = len(repetidos_df)
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write("=" * 20 + " REPORTE DE PERSONAS REPETIDAS EN EL REGISTRO " + "=" * 20 + "\n\n")
        archivo.write(f"Este reporte muestra las personas que aparecen más de una vez en el registro, identificadas por su número de documento.\n\nSe encontraron {num_repetidos} registros repetidos de un total de {total_personas} personas.\n\n")
        if not repetidos_df.empty:
            tabla_repetidos = tabulate(repetidos_df, headers='keys', tablefmt='grid', showindex=False)
            archivo.write(tabla_repetidos)
        else:
            archivo.write("No se encontraron personas repetidas en el registro.\n")
            print(f"No se encontraron personas repetidas. El archivo '{nombre_archivo}' ha sido creado.")

if __name__ == "__main__":
    ruta_archivo_xlsx = 'Archivo/Cuestionario Cabildo TATACHIO MIRABEL (Respuestas).xlsx'
    nombre_archivo_familias_txt = 'reportes/reportes_txt/reporte_familias.txt'
    nombre_archivo_un_miembro_txt = 'reportes/reportes_txt/reporte_1_miembro.txt'
    nombre_archivo_advertencias_txt = 'reportes/reportes_txt/reporte_advertencias.txt'
    nombre_archivo_repetidos_txt = 'reportes/reportes_txt/reporte_repetidos.txt'

    resultado_analisis = procesar_datos(ruta_archivo_xlsx)

    if isinstance(resultado_analisis, str):
        print(resultado_analisis)
    else:
        familias_multiples, familias_uno, lista_advertencias, total_personas, personas_repetidas = resultado_analisis

        generar_reporte_familias_txt(familias_multiples, nombre_archivo_familias_txt, total_personas)
        generar_reporte_un_miembro_txt(familias_uno, nombre_archivo_un_miembro_txt, total_personas)
        generar_reporte_advertencias_txt(lista_advertencias, nombre_archivo_advertencias_txt, total_personas)
        generar_reporte_repetidos_txt(personas_repetidas, nombre_archivo_repetidos_txt, total_personas)