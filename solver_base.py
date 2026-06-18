import json
import pulp
import subprocess
import os
import time
import csv

def resolver_instancia(ruta_archivo):
    # Medir el tiempo de inicio
    tiempo_inicio = time.perf_counter()
    
    with open(ruta_archivo, "r", encoding="latin-1") as f:
        data = json.load(f)

    nombre_inst = data['nombre']

    I = range(data['P_count'])
    J = range(data['CD_count'])
    K = range(data['ZD_count'])

    C = data['costos_P_CD']
    D = data['costos_CD_ZD']
    F = data['costos_fijos']
    S = data['cap_plantas']
    H = data['cap_centros']
    R = data['demandas']
    P_max = data['P_max']

    modelo = pulp.LpProblem(f"Mod_{nombre_inst}", pulp.LpMinimize)

    x = pulp.LpVariable.dicts("x", (I, J), lowBound=0, cat='Continuous')
    y = pulp.LpVariable.dicts("y", (J, K), lowBound=0, cat='Continuous')
    z = pulp.LpVariable.dicts("z", J, cat='Binary')

    modelo += (
        pulp.lpSum(F[j] * z[j] for j in J) +
        pulp.lpSum(C[i][j] * x[i][j] for i in I for j in J) +
        pulp.lpSum(D[j][k] * y[j][k] for j in J for k in K)
    ), "Costo"

    for i in I:
        modelo += pulp.lpSum(x[i][j] for j in J) <= S[i], f"Cp_{i}"
    for j in J:
        modelo += pulp.lpSum(x[i][j] for i in I) == pulp.lpSum(y[j][k] for k in K), f"Fl_{j}"
    for j in J:
        modelo += pulp.lpSum(y[j][k] for k in K) <= H[j] * z[j], f"Hb_{j}"
    for k in K:
        modelo += pulp.lpSum(y[j][k] for j in J) == R[k], f"Dm_{k}"
    
    modelo += pulp.lpSum(z[j] for j in J) <= P_max, "MaxCD"

    # Exportar y resolver
    archivo_mps = f"temp_{nombre_inst}.mps"
    modelo.writeMPS(archivo_mps)
    
    resultado = subprocess.run(["lp_solve", "-fmps", archivo_mps], capture_output=True, text=True)
    salida = resultado.stdout
    
    # Variables a recolectar
    estado = "Infactible"
    costo = 0.0
    abiertos = 0
    
    if "Value of objective function:" in salida:
        estado = "Optimal"
        lineas = salida.split('\n')
        for linea in lineas:
            if "Value of objective function:" in linea:
                costo = float(linea.split(':')[1].strip())
            elif linea.strip().startswith('z_'):
                partes = linea.split()
                if len(partes) >= 2 and float(partes[1]) > 0.5:
                    abiertos += 1
    
    if os.path.exists(archivo_mps):
        os.remove(archivo_mps)

    # Calcular tiempo total
    tiempo_fin = time.perf_counter()
    tiempo_ejecucion = round(tiempo_fin - tiempo_inicio, 4)
    
    print(f"[{nombre_inst:<10}] Estado: {estado:<8} | Costo: ${costo:,.0f} | CD Abiertos: {abiertos}/{P_max} | Tiempo: {tiempo_ejecucion}s")
    
    # ESTO ES LO QUE FALTABA: Retornar los datos al ciclo for
    return {
        "Instancia": nombre_inst,
        "Estado": estado,
        "Plantas": data['P_count'],
        "CD_Disponibles": data['CD_count'],
        "Zonas": data['ZD_count'],
        "Limite_P_Max": P_max,
        "CD_Abiertos": abiertos,
        "Costo_Total": costo,
        "Tiempo_Segundos": tiempo_ejecucion
    }

if __name__ == "__main__":
    carpeta_instancias = "instancias"
    resultados_totales = []
    
    print("=== INICIANDO PROCESAMIENTO MASIVO (15 INSTANCIAS) ===\n")
    
    archivos = [f for f in os.listdir(carpeta_instancias) if f.endswith('.json')]
    archivos.sort() 
    
    for archivo in archivos:
        ruta_completa = os.path.join(carpeta_instancias, archivo)
        datos_instancia = resolver_instancia(ruta_completa)
        resultados_totales.append(datos_instancia)
        
    archivo_csv = "resultados_proyecto.csv"
    columnas = ["Instancia", "Estado", "Plantas", "CD_Disponibles", "Zonas", "Limite_P_Max", "CD_Abiertos", "Costo_Total", "Tiempo_Segundos"]
    
    with open(archivo_csv, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(resultados_totales)
        
    print(f"\n=== PROCESO TERMINADO ===")
    print(f"Se han guardado los resultados en el archivo: '{archivo_csv}'")