from modelos.usuario import Usuario

class Empleado(Usuario):
    def __init__(self, id_usuario: int, nombre: str, email: str, cargo: str, tarifa_hora: float):
        # Invocamos al constructor de la clase base (Usuario)
        super().__init__(id_usuario, nombre, email)
        self._cargo = cargo
        self._tarifa_hora = tarifa_hora

    @property
    def cargo(self) -> str:
        return self._cargo

    @cargo.setter
    def cargo(self, nuevo_cargo: str):
        self._cargo = nuevo_cargo

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @tarifa_hora.setter
    def tarifa_hora(self, nueva_tarifa: float):
        if nueva_tarifa >= 0:
            self._tarifa_hora = nueva_tarifa
        else:
            raise ValueError("La tarifa por hora no puede ser negativa.")

    def obtener_detalles(self) -> str:
        """Polimorfismo: Extiende la información para incluir datos del cargo."""
        info_base = super().obtener_detalles()
        return f"{info_base} | Cargo: {self._cargo} | Tarifa/h: ${self._tarifa_hora:.2f}"