# Gerente hereda de Empleado e incluye gestión de equipo y bonificaciones.

from typing import Optional

from modelos.empleado import Empleado
from modelos.usuario import Usuario

class Gerente(Empleado):
    def __init__(
        self,
        id_empleado: int,
        nombre: str,
        email: str,
        tarifa_hora: float,
        bono_liderazgo: float = 1.0,
        usuario: Optional[Usuario] = None,
    ):
        super().__init__(
            id_empleado,
            nombre,
            email,
            cargo="Gerente",
            tarifa_hora=tarifa_hora,
            usuario=usuario,
        )
        self.bono_liderazgo = bono_liderazgo
        self._empleados_a_cargo = []

    @property
    def bono_liderazgo(self) -> float:
        return self._bono_liderazgo

    @bono_liderazgo.setter
    def bono_liderazgo(self, nuevo_bono: float):
        if nuevo_bono > 0:
            self._bono_liderazgo = nuevo_bono
        else:
            raise ValueError("El bono de liderazgo debe ser mayor que cero.")

    def asignar_empleado(self, empleado: Empleado):
        """Agrega un empleado al equipo a cargo del gerente."""
        if empleado not in self._empleados_a_cargo:
            self._empleados_a_cargo.append(empleado)

    def obtener_detalles(self) -> str:
        """Sobrescribe para mostrar detalles del bono y equipo a cargo."""
        info_base = super().obtener_detalles()
        return f"{info_base} | Bono: ${self._bono_liderazgo:.2f} | Equipo: {len(self._empleados_a_cargo)} empleados"