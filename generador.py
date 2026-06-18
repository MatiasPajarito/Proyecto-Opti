import random
import json
import os

# 1. La clase (Estructura de la instancia)
class InstanciaLogistica:
    def __init__(self, nombre, n_p, n_cd, n_zd):
        self.nombre = nombre
        self.P_count = n_p  
        self.CD_count = n_cd  
        self.ZD_count = n_zd 
        self.demandas = []
        self.cap_plantas = []
        self.cap_centros = []
        self.costos_fijos = []
        self.costos_P_CD = []
        self.costos_CD_ZD = []
        self.P_max = 0 # Límite máximo de centros operativos

# 2. Herramientas de formato
def formatear_matriz(matriz):
    filas = [f"        {row}" for row in matriz]
    return "[\n" + ",\n".join(filas) + "\n    ]"

def guardar_instancias_ordenado(instancias):
    if not os.path.exists("instancias"):
        os.makedirs("instancias")

    for inst in instancias:
        json_str = "{\n"
        json_str += f'    "nombre": "{inst.nombre}",\n'
        json_str += f'    "P_count": {inst.P_count},\n'
        json_str += f'    "CD_count": {inst.CD_count},\n'
        json_str += f'    "ZD_count": {inst.ZD_count},\n'
        json_str += f'    "demandas": {inst.demandas},\n'
        json_str += f'    "cap_plantas": {inst.cap_plantas},\n'
        json_str += f'    "cap_centros": {inst.cap_centros},\n'
        json_str += f'    "costos_fijos": {inst.costos_fijos},\n'
        json_str += f'    "P_max": {inst.P_max},\n'
        # Aplicamos el formato de tabla a las matrices de costos
        json_str += f'    "costos_P_CD": {formatear_matriz(inst.costos_P_CD)},\n'
        json_str += f'    "costos_CD_ZD": {formatear_matriz(inst.costos_CD_ZD)}\n'
        json_str += "}"

        with open(f"instancias/{inst.nombre}.json", "w", encoding="utf-8") as f:
            f.write(json_str)
    
    print(f"--> Éxito: {len(instancias)} archivos generados en la carpeta /instancias.")

# 3. Generador de datos
def generar_datos():
    # Rangos obligatorios de la Tabla 1
    config_rangos = {
        "Pequeña": {"P": (3, 10), "CD": (6, 12), "ZD": (8, 15)},
        "Mediana": {"P": (11, 20), "CD": (12, 24), "ZD": (16, 30)},
        "Grande":  {"P": (21, 35), "CD": (25, 40), "ZD": (31, 45)}
    }
    
    todas = []
    for tipo, rangos in config_rangos.items():
        for i in range(1, 6):  # 5 instancias por cada tamaño
            n_p = random.randint(*rangos["P"])
            n_cd = random.randint(*rangos["CD"])
            n_zd = random.randint(*rangos["ZD"])
            
            inst = InstanciaLogistica(f"{tipo}_{i}", n_p, n_cd, n_zd)
            
            # Factibilidad: Generar demandas primero
            inst.demandas = [random.randint(50, 200) for _ in range(n_zd)]
            total_demanda = sum(inst.demandas)
            
            # Factibilidad: Asegurar que Plantas > Demanda
            # Margen del 20% extra repartido entre las plantas
            oferta_minima_por_planta = (total_demanda * 1.2) // n_p
            inst.cap_plantas = [random.randint(int(oferta_minima_por_planta), int(oferta_minima_por_planta*1.5)) for _ in range(n_p)]
            
            # Costos fijos y límites
            inst.costos_fijos = [random.randint(2000, 8000) for _ in range(n_cd)] 
            
            # [CORRECCIÓN LOGÍSTICA]
            # Definimos P_max primero para saber cuál será nuestro "embudo" en la red.
            inst.P_max = random.randint(1, n_cd - 1) 
            
            # La capacidad de cada CD debe basarse en P_max para asegurar la factibilidad del flujo.
            # Dividimos la demanda total por P_max y le agregamos un 20% de holgura.
            cap_minima_cd = (total_demanda * 1.2) // inst.P_max
            inst.cap_centros = [random.randint(int(cap_minima_cd), int(cap_minima_cd*1.5)) for _ in range(n_cd)]
            
            # Matrices de costos
            inst.costos_P_CD = [[random.randint(5, 30) for _ in range(n_cd)] for _ in range(n_p)]
            inst.costos_CD_ZD = [[random.randint(5, 30) for _ in range(n_zd)] for _ in range(n_cd)]
            
            todas.append(inst)
    return todas

# 4. main
if __name__ == "__main__":
    print("--- Generador de Instancias Logísticas INF292 ---")
    
    # Generacion de datos
    lista_final = generar_datos()
    
    # Guardado de datos de manera ordenada
    guardar_instancias_ordenado(lista_final)
    
    # Tabla resumen
    print("\nTABLA RESUMEN PARA EL INFORME:")
    print(f"{'Nombre':<12} | {'Plantas':<7} | {'CDs':<4} | {'Zonas':<5} | {'Demanda Total':<13} | {'Cap. Total':<10} |")
    print("-" * 75)
    for inst in lista_final:
        d_total = sum(inst.demandas)
        c_total = sum(inst.cap_plantas)
        print(f"{inst.nombre:<12} | {inst.P_count:<7} | {inst.CD_count:<4} | {inst.ZD_count:<5} | {d_total:<13} | {c_total:<10} |")