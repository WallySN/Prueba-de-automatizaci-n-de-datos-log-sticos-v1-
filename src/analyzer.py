"""
analyzer.py
Detective estadístico: extrae patrones de probabilidad de las ventas reales.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class VentasAnalyzer:
    """
    Esta clase analiza un DataFrame de ventas y extrae las distribuciones
    de probabilidad necesarias para generar nuevas ventas realistas.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Constructor: recibe el DataFrame de ventas limpio.
        """
        self.df = df.copy()
        self.distribuciones: Dict = {}
        
    def analizar_productos(self) -> Dict:
        """
        Extrae la probabilidad de venta de cada producto.
        Ejemplo: {'Vestido': 0.265, 'Zapatos': 0.265, ...}
        """
        conteo = self.df['Producto'].value_counts(normalize=True)
        return {
            'productos': conteo.index.tolist(),
            'probabilidades': conteo.values.tolist()
        }
    
    def analizar_ciudades(self) -> Dict:
        """
        Extrae la probabilidad de venta por ciudad.
        """
        conteo = self.df['Ciudad'].value_counts(normalize=True)
        return {
            'ciudades': conteo.index.tolist(),
            'probabilidades': conteo.values.tolist()
        }
    
    def analizar_cantidades(self) -> Dict[str, Dict]:
        """
        Para cada producto, extrae el rango y promedio de cantidades vendidas.
        """
        resultado = {}
        for producto in self.df['Producto'].unique():
            datos = self.df[self.df['Producto'] == producto]['Cantidad']
            resultado[producto] = {
                'min': int(datos.min()),
                'max': int(datos.max()),
                'media': float(datos.mean()),
                'std': float(datos.std())
            }
        return resultado
    
    def analizar_precios(self) -> Dict[str, Dict]:
        """
        Para cada producto, extrae el rango de precios unitarios reales.
        """
        resultado = {}
        for producto in self.df['Producto'].unique():
            datos = self.df[self.df['Producto'] == producto]['Precio_Unitario']
            resultado[producto] = {
                'min': int(datos.min()),
                'max': int(datos.max()),
                'media': float(datos.mean()),
                'std': float(datos.std())
            }
        return resultado
    
    def analizar_frecuencia(self) -> Dict:
        """
        Calcula cada cuántos días ocurre una venta en promedio.
        """
        fechas = self.df['Fecha'].sort_values().reset_index(drop=True)
        dias_entre = fechas.diff().dt.days.dropna()
        return {
            'media_dias': float(dias_entre.mean()),
            'std_dias': float(dias_entre.std())
        }
    
    def analizar_todo(self) -> Dict:
        """
        Ejecuta TODOS los análisis y guarda el resultado en self.distribuciones.
        Este es el "informe completo del detective".
        """
        self.distribuciones = {
            'productos': self.analizar_productos(),
            'ciudades': self.analizar_ciudades(),
            'cantidades': self.analizar_cantidades(),
            'precios': self.analizar_precios(),
            'frecuencia': self.analizar_frecuencia()
        }
        return self.distribuciones
    
    def mostrar_resumen(self):
        """
        Imprime un resumen bonito en la terminal (para debugging).
        """
        if not self.distribuciones:
            self.analizar_todo()
        
        d = self.distribuciones
        
        print("=" * 50)
        print("📊 INFORME DEL DETECTIVE ESTADÍSTICO")
        print("=" * 50)
        
        print("\n📦 PROBABILIDAD POR PRODUCTO:")
        for p, prob in zip(d['productos']['productos'], d['productos']['probabilidades']):
            print(f"   {p}: {prob:.1%}")
        
        print("\n🏙️ PROBABILIDAD POR CIUDAD:")
        for c, prob in zip(d['ciudades']['ciudades'], d['ciudades']['probabilidades']):
            print(f"   {c}: {prob:.1%}")
        
        print("\n📊 CANTIDADES POR PRODUCTO:")
        for prod, info in d['cantidades'].items():
            print(f"   {prod}: {info['min']}-{info['max']} unidades (media: {info['media']:.1f})")
        
        print("\n💰 PRECIOS POR PRODUCTO:")
        for prod, info in d['precios'].items():
            print(f"   {prod}: ${info['min']:,} - ${info['max']:,} (media: ${info['media']:,.0f})")
        
        print(f"\n⏱️ FRECUENCIA: cada {d['frecuencia']['media_dias']:.1f} días (±{d['frecuencia']['std_dias']:.1f})")
        print("=" * 50)


# ============================================
# PRUEBA RÁPIDA (solo si ejecutas este archivo directamente)
# ============================================
if __name__ == "__main__":
    from load_data import carga_ventas
    
    RUTA = "data/base_datos_empresa_ropa.xlsx"
    ventas_df = carga_ventas(RUTA)
    
    detective = VentasAnalyzer(ventas_df)
    detective.mostrar_resumen()