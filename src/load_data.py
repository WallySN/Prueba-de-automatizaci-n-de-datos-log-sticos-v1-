"""
load_data.py
carga y limpia los datos de excel de la empresa de ropa
"""

import pandas as pd


def carga_ventas(ruta: str) -> pd.DataFrame:
    """
    carga la hoja 'Ventas' del excel y limpia los encabezados
duplicados
    """
    df = pd.read_excel(ruta, sheet_name='Ventas')

    df = df.iloc[1:].reset_index(drop=True)

    # Renombrar columnas
    df.columns = ['ID_Venta', 'Fecha', 'Producto', 'Cantidad',
                   'Precio_Unitario', 'Total', 'Ciudad']

    # Convertir tipos de datos
    df['Cantidad'] = df['Cantidad'].astype(int)
    df['Precio_Unitario'] = df['Precio_Unitario'].astype(float)
    df['Total'] = df ['Total'].astype(float)
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    return df 


if __name__ == "__main__":
    #Prueba rapida
    RUTA = "data/base_datos_empresa_ropa.xlsx"
    ventas = carga_ventas(RUTA)
    print(f"✅ Ventas cargadas: {len(ventas)} registros")
    print(ventas.head())