from datetime import datetime
from modelos.empleado import Empleado
from modelos.proyecto import Proyecto

class RegistroTiempo:
    def __init__(self, id_registro: int, empleado: Empleado, proyecto: Proyecto, horas_trabajadas: float, fecha: str = None, descripcion: str = ""):
        self._id_registro = id_registro
        self._empleado = empleado
        self._proyecto = proyecto
        # Usar la propiedad 'horas_trabajadas' ejecuta la validación del setter durante la creación
        self.horas_trabajadas = horas_trabajadas  
        self._fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d")
        self._descripcion = descripcion

    @property
    def id_registro(self) -> int:
        return self._id_registro

    @property
    def empleado(self) -> Empleado:
        return self._empleado

    @property
    def proyecto(self) -> Proyecto:
        return self._proyecto

    @property
    def horas_trabajadas(self) -> float:
        return self._horas_trabajadas

    @horas_trabajadas.setter
    def horas_trabajadas(self, horas: float):
        if horas > 0:
            self._horas_trabajadas = horas
        else:
            raise ValueError("Las horas trabajadas deben ser mayores a 0.")

    def calcular_costo_laboral(self) -> float:
        """Calcula el costo del registro según la tarifa por hora del empleado."""
        return self._horas_trabajadas * self._empleado.tarifa_hora

    def obtener_detalles(self) -> str:
        costo = self.calcular_costo_laboral()
        return (f"Registro [{self._id_registro}] ({self._fecha}): {self._empleado.nombre} -> "
                f"Proyecto '{self._proyecto.nombre}' | Horas: {self._horas_trabajadas}h | Costo: ${costo:.2f}")

    def __str__(self) -> str:
        return self.obtener_detalles()