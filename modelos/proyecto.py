from typing import List
from modelos.empleado import Empleado

class Proyecto:
    def __init__(self, id_proyecto: int, nombre: str, presupuesto: float, estado: str = "Planificación"):
        self._id_proyecto = id_proyecto
        self._nombre = nombre
        self._presupuesto = presupuesto
        self._estado = estado  # Ejemplo: 'Planificación', 'En Progreso', 'Completado'
        self._equipo: List[Empleado] = []

    @property
    def id_proyecto(self) -> int:
        return self._id_proyecto

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def presupuesto(self) -> float:
        return self._presupuesto

    @presupuesto.setter
    def presupuesto(self, nuevo_presupuesto: float):
        if nuevo_presupuesto >= 0:
            self._presupuesto = nuevo_presupuesto
        else:
            raise ValueError("El presupuesto no puede ser negativo.")

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, nuevo_estado: str):
        self._estado = nuevo_estado

    def asignar_miembro(self, empleado: Empleado):
        """Agrega un empleado o gerente al equipo del proyecto."""
        if empleado not in self._equipo:
            self._equipo.append(empleado)

    def obtener_detalles(self) -> str:
        return f"Proyecto [{self._id_proyecto}]: {self._nombre} | Estado: {self._estado} | Presupuesto: ${self._presupuesto:,.2f} | Miembros: {len(self._equipo)}"

    def __str__(self) -> str:
        return self.obtener_detalles()