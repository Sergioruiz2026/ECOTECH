#Esta clase representa un departamento de la empresa (ej. Tecnología, Operaciones), 
# el cual cuenta con un gerente a cargo y una lista de empleados asociados.

from typing import List, Optional
from modelos.empleado import Empleado
from modelos.gerente import Gerente

class Departamento:
    def __init__(self, id_departamento: int, nombre: str, gerente: Optional[Gerente] = None):
        self._id_departamento = id_departamento
        self._nombre = nombre
        self._gerente = gerente
        self._empleados: List[Empleado] = []

    @property
    def id_departamento(self) -> int:
        return self._id_departamento

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        if nuevo_nombre.strip():
            self._nombre = nuevo_nombre
        else:
            raise ValueError("El nombre del departamento no puede estar vacío.")

    @property
    def gerente(self) -> Optional[Gerente]:
        return self._gerente

    @gerente.setter
    def gerente(self, nuevo_gerente: Gerente):
        self._gerente = nuevo_gerente

    @property
    def empleados(self) -> List[Empleado]:
        return self._empleados.copy()

    def agregar_empleado(self, empleado: Empleado):
        """Asigna un empleado al departamento."""
        if empleado not in self._empleados:
            self._empleados.append(empleado)
            if self._gerente:
                self._gerente.asignar_empleado(empleado)

    def remover_empleado(self, id_empleado: int):
        """Elimina un empleado del departamento por su ID."""
        self._empleados = [e for e in self._empleados if e.id_usuario != id_empleado]

    def obtener_detalles(self) -> str:
        nom_gerente = self._gerente.nombre if self._gerente else "Sin Gerente asignado"
        return f"Depto [{self._id_departamento}]: {self._nombre} | Gerente: {nom_gerente} | Cant. Empleados: {len(self._empleados)}"

    def __str__(self) -> str:
        return self.obtener_detalles()