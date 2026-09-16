# Empleado es una ficha laboral independiente de la cuenta de Usuario.

import hashlib
from typing import Optional

from modelos.usuario import Usuario


class Empleado:
    def __init__(
        self,
        id_empleado: int,
        nombre: str,
        email: str,
        cargo: str,
        tarifa_hora: float,
        usuario: Optional[Usuario] = None,
    ):
        self._id_empleado = id_empleado
        self.nombre = nombre
        self.email = email
        self._cargo = cargo
        self.tarifa_hora = tarifa_hora
        self._usuario = usuario

    @property
    def id_empleado(self) -> int:
        return self._id_empleado

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        if not isinstance(valor, str):
            raise ValueError("El correo electrónico debe ser una cadena de texto válida.")

        valor = valor.strip().lower()
        if not Usuario.PATRON_EMAIL.fullmatch(valor):
            raise ValueError(
                f"El correo electrónico '{valor}' no es válido. "
                "Debe tener un formato correcto (ej: usuario@dominio.com)."
            )
        self._email = valor

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
        if nueva_tarifa > 0:
            self._tarifa_hora = nueva_tarifa
        else:
            raise ValueError("La tarifa por hora debe ser mayor que cero.")

    @property
    def usuario(self) -> Optional[Usuario]:
        return self._usuario

    def asociar_usuario(self, usuario: Usuario):
        if not isinstance(usuario, Usuario):
            raise TypeError("La asociación debe realizarse con un Usuario válido.")
        self._usuario = usuario

    def desasociar_usuario(self):
        self._usuario = None

    def obtener_email_cifrado(self) -> str:
        partes = self._email.split("@")
        if len(partes) != 2:
            return self._email

        usuario_local, dominio = partes
        if Usuario.PATRON_HASH_EMAIL.fullmatch(usuario_local):
            return self._email

        hash_local = hashlib.sha256(usuario_local.encode("utf-8")).hexdigest()[:16]
        return f"{hash_local}@{dominio}"

    def obtener_detalles(self) -> str:
        detalles = (
            f"ID: {self._id_empleado} | Nombre: {self._nombre} | "
            f"Email: {self._email} | Cargo: {self._cargo} | "
            f"Tarifa/h: ${self._tarifa_hora:.2f}"
        )
        if self._usuario:
            detalles += f" | Email usuario: {self._usuario.email}"
        return detalles