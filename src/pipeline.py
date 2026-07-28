"""
pipeline.py
Jefe de planta: coordina todo el flujo de trabajo.
Carga → Analiza → Genera → Guarda
"""

import pandas as pd
from datetime import datetime
from pathlib import Path

from load_data import carga_ventas
from analyzer import VentasAnalyzer
from generator import VentasGenerator


class VentasPipeline:
    """
    Esta clase es el 'jefe de planta'. 
    Conecta los 3 módulos y ejecuta el flujo completo.
    """
    
    def __init__(self, ruta_datos: str, ruta_output: str = "output"):
        """
        Constructor: recibe la ruta del Excel y dónde guardar resultados.
        """
        self.ruta_datos = ruta_datos
        self.ruta_output = Path(ruta_output)
        self.ruta_output.mkdir(exist_ok=True)  # Crear carpeta si no existe
        
        # Estos se llenarán durante la ejecución
        self.ventas_originales = None
        self.distribuciones = None
        self.ventas_nuevas = None
        
    def ejecutar(self, cantidad_nuevas: int = 10) -> pd.DataFrame:
        """
        Ejecuta el pipeline completo paso a paso.
        
        Args:
            cantidad_nuevas: Cuántas ventas nuevas generar
        
        Returns:
            DataFrame con las ventas nuevas generadas
        """
        print("=" * 60)
        print("🏭 PIPELINE DE VENTAS PROBABILÍSTICAS")
        print("=" * 60)
        
        # ═══════════════════════════════════════════════════════
        # PASO 1: CARGAR DATOS (Recepción)
        # ═══════════════════════════════════════════════════════
        print("\n📥 [PASO 1/4] Cargando datos originales...")
        self.ventas_originales = carga_ventas(self.ruta_datos)
        print(f"   ✅ {len(self.ventas_originales)} ventas cargadas")
        
        # ═══════════════════════════════════════════════════════
        # PASO 2: ANALIZAR (Laboratorio)
        # ═══════════════════════════════════════════════════════
        print("\n🔬 [PASO 2/4] Analizando patrones estadísticos...")
        detective = VentasAnalyzer(self.ventas_originales)
        self.distribuciones = detective.analizar_todo()
        print("   ✅ Distribuciones de probabilidad extraídas")
        
        # Mostrar resumen rápido
        prod = self.distribuciones['productos']
        print(f"   📦 Productos analizados: {len(prod['productos'])}")
        print(f"   🏙️ Ciudades analizadas: {len(self.distribuciones['ciudades']['ciudades'])}")
        
        # ═══════════════════════════════════════════════════════
        # PASO 3: GENERAR (Fábrica)
        # ═══════════════════════════════════════════════════════
        print(f"\n🏭 [PASO 3/4] Generando {cantidad_nuevas} ventas nuevas...")
        fabrica = VentasGenerator(self.distribuciones)
        self.ventas_nuevas = fabrica.generar_ventas(cantidad_nuevas)
        print(f"   ✅ {cantidad_nuevas} ventas generadas")
        
        # ═══════════════════════════════════════════════════════
        # PASO 4: GUARDAR (Almacén)
        # ═══════════════════════════════════════════════════════
        print("\n💾 [PASO 4/4] Guardando resultados...")
        
        # Crear nombre de archivo con fecha y hora
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"ventas_nuevas_{timestamp}.xlsx"
        ruta_salida = self.ruta_output / nombre_archivo
        
        # Guardar en Excel
        self.ventas_nuevas.to_excel(ruta_salida, index=False, sheet_name='Ventas_Nuevas')
        print(f"   ✅ Guardado en: {ruta_salida}")
        
        # También guardar un resumen en CSV por si acaso
        ruta_csv = self.ruta_output / f"ventas_nuevas_{timestamp}.csv"
        self.ventas_nuevas.to_csv(ruta_csv, index=False)
        print(f"   ✅ Backup CSV: {ruta_csv}")
        
        print("\n" + "=" * 60)
        print("🎉 PIPELINE COMPLETADO CON ÉXITO")
        print("=" * 60)
        
        return self.ventas_nuevas
    
    def mostrar_muestra(self, n: int = 5):
        """
        Muestra una muestra de las ventas generadas.
        """
        if self.ventas_nuevas is None:
            print("❌ Primero ejecuta el pipeline")
            return
        
        print(f"\n📋 MUESTRA DE {n} VENTAS GENERADAS:")
        print(self.ventas_nuevas.head(n).to_string(index=False))


# ============================================
# PRUEBA RÁPIDA
# ============================================
if __name__ == "__main__":
    # Crear el jefe de planta
    jefe = VentasPipeline(
        ruta_datos="data/base_datos_empresa_ropa.xlsx",
        ruta_output="output"
    )
    
    # Ejecutar: generar 20 ventas nuevas
    nuevas_ventas = jefe.ejecutar(cantidad_nuevas=20)
    
    # Mostrar muestra
    jefe.mostrar_muestra(n=5)