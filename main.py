from buscar_bid import buscar_trabajos_bid
from buscar_bm import buscar_trabajos_bm

import pandas as pd


# Descargar trabajos de ambas fuentes
trabajos_bid = buscar_trabajos_bid()
trabajos_bm = buscar_trabajos_bm()

# Combinar ambas listas
trabajos = []

trabajos.extend(trabajos_bid)
trabajos.extend(trabajos_bm)

# Crear DataFrame consolidado
df = pd.DataFrame(trabajos)

# Exportar archivo consolidado
df.to_excel(
    "resultados/trabajos_consolidados.xlsx",
    index=False
)

print(f"Se descargaron {len(df)} trabajos en total.")
print(f"BID: {len(trabajos_bid)} trabajos.")
print(f"Banco Mundial: {len(trabajos_bm)} trabajos.")