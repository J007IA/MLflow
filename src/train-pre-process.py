import pandas as pd

# --- Cargar datos ---
clientes = pd.read_csv('../exploration-part/data/raw/train_clientes_sample.csv')
requerimientos = pd.read_csv('../exploration-part/data/raw/train_requerimientos_sample.csv')

# --- Agregar info de requerimientos por cliente ---
# 1. Total requerimientos por cliente (últimos 6 meses)
total_reqs = requerimientos.groupby('ID_CORRELATIVO').size().rename('TOTAL_REQUERIMIENTOS')

# 2. Total reclamos
total_reclamos = requerimientos[requerimientos['TIPO_REQUERIMIENTO2'] == 'Reclamo'] \
                .groupby('ID_CORRELATIVO').size().rename('TOTAL_RECLAMOS')

# 3. Porcentaje reclamos / total requerimientos
porc_reclamos = (total_reclamos / total_reqs).fillna(0).rename('PORC_RECLAMOS')

# 4. Dicteman procede (cuántos 'PROCEDE' vs total)
dictamen_procede = requerimientos[requerimientos['DICTAMEN'].str.upper() == 'PROCEDE'] \
                    .groupby('ID_CORRELATIVO').size().rename('TOTAL_PROCDE')

porc_procede = (dictamen_procede / total_reqs).fillna(0).rename('PORC_PROCDE')

# 5. Requerimientos promedio por mes (contar meses activos)
meses_activos = requerimientos.groupby('ID_CORRELATIVO')['CODMES'].nunique().rename('MESES_ACTIVOS')

req_prom_mes = (total_reqs / meses_activos).fillna(0).rename('REQ_PROM_MES')

# --- Combinar todas las agregaciones en un solo DataFrame ---
req_agg = pd.concat([total_reqs, total_reclamos, porc_reclamos, dictamen_procede, porc_procede, meses_activos, req_prom_mes], axis=1).fillna(0)

# --- Unir con tabla de clientes ---
df_final = clientes.merge(req_agg, on='ID_CORRELATIVO', how='left').fillna({
    'TOTAL_REQUERIMIENTOS':0, 
    'TOTAL_RECLAMOS':0, 
    'PORC_RECLAMOS':0,
    'TOTAL_PROCDE':0,
    'PORC_PROCDE':0,
    'MESES_ACTIVOS':0,
    'REQ_PROM_MES':0
})

# --- Ejemplo de salida ---
print(df_final.head())

# --- Exportar a CSV ---
df_final.to_csv('../exploration-part/data/pre-processed/train_clientes_features.csv', index=False)
