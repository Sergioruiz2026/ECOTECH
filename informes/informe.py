from abc import ABC, abstractmethod
from typing import List, Dict, Any

class Informe(ABC):
    #Clase base abstracta para la generación de informes en ECOTECH.
    #Define la estructura que deben implementar los exportadores (PDF, Excel, etc.).
    
    def __init__(self, titulo: str, datos: List[Dict[str, Any]]):
        self.titulo = titulo
        self.datos = datos

    @abstractmethod
    def generar(self, ruta_archivo: str) -> bool:
        
    #Método abstracto para exportar el informe a un archivo específico.
    #param ruta_archivo: Ruta de destino para guardar el archivo generado.
    #:return: True si la generación fue exitosa, False en caso contrario.        :return: True si la generación fue exitosa, False en caso contrario.
    
        pass
