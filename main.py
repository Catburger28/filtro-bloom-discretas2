import math
import hashlib

class FiltroBloom:
    def __init__(self, m, n):
        """
        Inicializa el filtro.
        m = tamaño del arreglo de bits
        n = número esperado de elementos a insertar
        """
        self.m = m
        self.n = n
        
        # 1. Determinación del k óptimo
        # La fórmula es k = (m/n) * ln(2)
        k_teorico = (m / n) * math.log(2)
        self.k = max(1, round(k_teorico)) 
        
        # Arreglo de bits inicializado en 0
        self.bit_array = [0] * m

    def _obtener_indices(self, elemento):
        """Genera 'k' índices hash para el elemento."""
        indices = []
        for i in range(self.k):
            elemento_modificado = f"{elemento}_{i}".encode('utf-8')
            hash_hex = hashlib.sha256(elemento_modificado).hexdigest()
            indice = int(hash_hex, 16) % self.m
            indices.append(indice)
        return indices

    def insertar(self, elemento):
        """Inserta un elemento encendiendo los bits correspondientes."""
        for indice in self._obtener_indices(elemento):
            self.bit_array[indice] = 1

    def verificar(self, elemento):
        """Verifica si el elemento está en el filtro. Devuelve True si es posible, False si seguro no está."""
        for indice in self._obtener_indices(elemento):
            if self.bit_array[indice] == 0:
                return False
        return True

def simulacion_cargas():
    """
    2. Simulación de Falsos Positivos bajo distintas cargas de datos.
    Mantenemos un tamaño de filtro fijo y variamos el número de elementos insertados.
    """
    m_bits = 10000 # Tamaño de memoria del filtro fijo
    cargas_elementos_n = [500, 1000, 2000, 5000] # Distintas cargas de datos para estresar el sistema
    consultas_falsas = 1000 # Cantidad de pruebas con datos inexistentes para medir el error

    print("\n--- EVALUACION DE RENDIMIENTO DEL FILTRO DE BLOOM ---")
    print(f"Memoria asignada (m) = {m_bits} bits")
    print(f"Consultas de prueba por escenario = {consultas_falsas}\n")
    print(f"{'Carga (n)':<12} | {'k Optimo':<10} | {'Tasa Teorica':<15} | {'Tasa Empirica':<15}")
    print("-" * 58)

    for n in cargas_elementos_n:
        filtro = FiltroBloom(m_bits, n)
        
        # Insertar los 'n' elementos válidos
        for i in range(n):
            filtro.insertar(f"usuario_valido_{i}")
            
        # Simulación: Consultar elementos que sabemos que NO están para forzar falsos positivos
        falsos_positivos_detectados = 0
        for i in range(consultas_falsas):
            if filtro.verificar(f"hacker_invalido_{i}"):
                falsos_positivos_detectados += 1
                
        # Calcular tasa empírica
        tasa_empirica = falsos_positivos_detectados / consultas_falsas
        
        # Calcular tasa teórica para comparar: p = (1 - e^(-k*n/m))^k
        tasa_teorica = (1 - math.exp(-filtro.k * n / m_bits)) ** filtro.k
        
        print(f"{n:<12} | {filtro.k:<10} | {tasa_teorica:<15.4%} | {tasa_empirica:<15.4%}")
    print("\n")

if __name__ == "__main__":
    simulacion_cargas()