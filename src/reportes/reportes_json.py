import json
from ..procesamiento import procesar_datos
import os

def generar_reporte_familias_json(familias, nombre_archivo, total_personas):
    num_familias = len(familias)
    reporte = {
        "titulo": "REPORTE DE FAMILIAS CON MÁS DE UN MIEMBRO",
        "total_familias": num_familias,
        "total_personas_en_familias": sum(len(data['miembros']) + 1 for data in familias.values()),
        "total_personas_analizadas": total_personas,
        "familias": []
    }
    for jefe_cedula, data in familias.items():
        familia_data = {
            "cedula_jefe_familia": jefe_cedula,
            "jefe_de_familia": {"documento": data['jefe'][0], "nombre_completo": data['jefe'][1]},
            "miembros_de_familia": data['miembros'].to_dict(orient='records')
        }
        reporte["familias"].append(familia_data)

    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(reporte, archivo, indent=4, ensure_ascii=False)
    print(f"El reporte de familias con más de 1 miembro ha sido guardado en '{nombre_archivo}'.")

def generar_reporte_un_miembro_json(familias, nombre_archivo, total_personas):
    num_jefes_solos = len(familias)
    reporte = {
        "titulo": "REPORTE DE JEFES DE FAMILIA REGISTRADOS SIN OTROS MIEMBROS",
        "descripcion": "Esta tabla muestra a los jefes de familia que se registraron como el único miembro de su núcleo familiar. Esto podría indicar que faltan miembros por registrar o que realmente son familias unipersonales.",
        "total_jefes_solos": num_jefes_solos,
        "total_personas_analizadas": total_personas,
        "jefes_de_familia_solos": []
    }
    for jefe_cedula, data in familias.items():
        reporte["jefes_de_familia_solos"].append({
            "cedula_jefe": data['jefe'][0],
            "nombre_jefe": data['jefe'][1]
        })

    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(reporte, archivo, indent=4, ensure_ascii=False)
    print(f"El reporte de jefes de familia registrados sin otros miembros ha sido guardado en '{nombre_archivo}'.")

def generar_reporte_advertencias_json(advertencias, nombre_archivo, total_personas):
    num_advertencias = len(advertencias)
    reporte = {
        "titulo": "REPORTE DE ADVERTENCIAS EN LOS REGISTROS DE FAMILIA",
        "descripcion": "No se encontró ningún jefe de familia asociado a estas persona. Se recomienda revisar la cédula del jefe de familia.",
        "total_advertencias": num_advertencias,
        "total_personas_analizadas": total_personas,
        "advertencias": []
    }
    for adv in advertencias:
        advertencia_data = {
            "cedula_jefe_familia": adv[0],
            "nombre_completo_persona": adv[1],
            "cedula_persona": adv[2]        
        }
        reporte["advertencias"].append(advertencia_data)

    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(reporte, archivo, indent=4, ensure_ascii=False)
    print(f"El reporte de advertencias ha sido guardado en '{nombre_archivo}'.")

def generar_reporte_repetidos_json(repetidos_df, nombre_archivo, total_personas):
    num_repetidos = len(repetidos_df)
    reporte = {
        "titulo": "REPORTE DE PERSONAS REPETIDAS EN EL REGISTRO",
        "descripcion": f"Este reporte muestra las personas que aparecen más de una vez en el registro, identificadas por su número de documento. Se encontraron {num_repetidos} registros repetidos de un total de {total_personas} personas.",
        "total_registros_repetidos": num_repetidos,
        "total_personas_analizadas": total_personas,
        "personas_repetidas": []
    }
    if not repetidos_df.empty:
        for index, row in repetidos_df.iterrows():
            reporte["personas_repetidas"].append({
                "cedula_jefe_familia": row['Cedula de jefe(a) de Familia'],
                "nombre_completo_persona": row['Nombre Completo Persona'],
                "cedula_persona": row['Cedula Persona'],
                "cantidad_repeticiones": row['Cantidad']
            })

    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(reporte, archivo, indent=4, ensure_ascii=False)
    print(f"El reporte de personas repetidas ha sido guardado en '{nombre_archivo}'.")

if __name__ == "__main__":
    ruta_archivo_xlsx = 'Archivo/Cuestionario Cabildo TATACHIO MIRABEL (Respuestas).xlsx'
    ruta_base_json = 'reportes/reportes_json'
    os.makedirs(ruta_base_json, exist_ok=True)
    nombre_archivo_familias_json = os.path.join(ruta_base_json, 'reporte_familias.json')
    nombre_archivo_un_miembro_json = os.path.join(ruta_base_json, 'reporte_1_miembro.json')
    nombre_archivo_advertencias_json = os.path.join(ruta_base_json, 'reporte_advertencias.json')
    nombre_archivo_repetidos_json = os.path.join(ruta_base_json, 'reporte_repetidos.json')

    resultado_analisis = procesar_datos(ruta_archivo_xlsx)

    if isinstance(resultado_analisis, str):
        print(resultado_analisis)
    else:
        familias_multiples, familias_uno, lista_advertencias, total_personas, personas_repetidas = resultado_analisis

        generar_reporte_familias_json(familias_multiples, nombre_archivo_familias_json, total_personas)
        generar_reporte_un_miembro_json(familias_uno, nombre_archivo_un_miembro_json, total_personas)
        generar_reporte_advertencias_json(lista_advertencias, nombre_archivo_advertencias_json, total_personas)
        generar_reporte_repetidos_json(personas_repetidas, nombre_archivo_repetidos_json, total_personas)