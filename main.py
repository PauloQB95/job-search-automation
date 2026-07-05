from buscar_bid import buscar_trabajos_bid

import pandas as pd

trabajos = buscar_trabajos_bid()

df = pd.DataFrame(trabajos)

df.to_excel(
    "resultados/trabajos_bid.xlsx",
    index=False
)

print(f"Se descargaron {len(df)} trabajos.")