"""
generator.py
Fábrica de ventas: usa las reglas del detective para crear ventas nuevas.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, List
from analyzer import VentasAnalyzer


class VentasGenerator:
    """
    Esta clase genera nuevas ventas basándose en las distribuciones
    de probabilidad extraídas por el VentasAnalyzer.
    """
    def __init__(self, distribuciones: dict):
        """
        Constructor: recibe el 'informe del detective' (las distribuciones).
        """
        self.dist = distribuciones
        self.ultima_fecha = datetime(2026, 6, 30)
        self.contador_id = 50

    def _elegir_producto(self) -> str:
        """
        Gira la ruleta de productos y devuelve uno según sus probabilidades.
        """
        productos = self.dist['productos']['productos']
        probs = self.dist['productos']['probabilidades']
        return np.random.choice(productos, p=probs)

    def _elegir_ciudad(self) -> str:
        """
        Gira la ruleta de ciudades.
        """
        ciudades =self.dist['ciudades']['ciudades']
        probs = self.dist['ciudades']['probabilidades']
        return np.random.choice(ciudades, p=probs)

    def _elegir_cantidad(self, producto: str) -> int:
        """
        Elige una cantidad dentro del rango real de ese producto.
        """
        info = self.dist['precios'][producto]
        min_cant = info['min']
        max_cant = info['max']
        return round(random.uniform(min_cant, max_cant), 0)

    def _elegir_precio(self, producto: str) -> float:
        """
        Elige un precio unitario dentro del rango real de ese producto.
        """
        info = self.dist['precios'][producto]
        min_precio = info['min']
        max_precio = info['max']
        return round(random.uniform(min_precio, max_precio), 0)
    
    def _siguiente_fecha(self) -> datetime:
        """
        Calcula la siguiente fecha sumando días al azar,
        respetando la frecuencia real de ventas.
        """
        media_dias = self.dist['frecuencia']['media_dias']
        std_dias = self.dist['frecuencia']['std_dias']

        # Elegimos días al azar, pero cerca del promedio real
        dias_a_sumar = max(1, int(random.gauss(media_dias, std_dias)))
        self.ultima_fecha += timedelta(days=dias_a_sumar)
        return self.ultima_fecha

    def generar_venta(self) -> dict:
        """
        Genera UNA venta nueva girando todas las ruletas.
        """
        self.contador_id += 1
        producto = self._elegir_producto()
        cantidad = self._elegir_cantidad(producto)
        precio = self._elegir_precio(producto)
        total = cantidad * precio
        ciudad = self._elegir_ciudad()
        fecha = self._siguiente_fecha()

        return {
            'ID_Venta': self.contador_id,
            'Fecha': fecha.strftime('%Y-%m-%d'),
            'Producto': producto,
            'Cantidad': cantidad,
            'Precio_Unitario': int(precio),
            'Total': int(total),
            'Ciudad': ciudad 
        }

    def generar_ventas(self, cantidad: int) -> pd.DataFrame:
        """
        Genera VARIAS ventas nuevas y las devuelve como DataFrame.
        """
        ventas_nuevas = []
        for _ in range(cantidad):
            ventas_nuevas.append(self.generar_venta())

        return pd.DataFrame(ventas_nuevas)


# ============================================
# PRUEBA RÁPIDA
# ============================================
if __name__ == "__main__":
    from load_data import carga_ventas
    
    # 1. Cargar datos
    RUTA = "data/base_datos_empresa_ropa.xlsx"
    ventas_df = carga_ventas(RUTA)
    
    # 2. Analizar (detective)
    detective = VentasAnalyzer(ventas_df)
    distribuciones = detective.analizar_todo()
    
    # 3. Generar (fábrica)
    fabrica = VentasGenerator(distribuciones)
    nuevas = fabrica.generar_ventas(10)  # Generamos 10 ventas nuevas
    
    print("=" * 60)
    print("🎰 10 VENTAS NUEVAS GENERADAS PROBABILÍSTICAMENTE")
    print("=" * 60)
    print(nuevas.to_string(index=False))
    print("=" * 60)