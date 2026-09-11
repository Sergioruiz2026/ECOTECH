#Esta clase define las propiedades comunes a cualquier persona dentro del sistema.

class Usuario:
    def __init__(self, id_usuario: int, nombre: str, email: str):
        self._id_usuario = id_usuario
        self._nombre = nombre
        self._email = email

    # Getters y Setters:método que se utilizan en POO para consultar y 
    # modificar los atributos de una clase de manera controlada.
    
    @property
    def id_usuario(self) -> int:
        return self._id_usuario

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        if nuevo_nombre.strip():
            self._nombre = nuevo_nombre
        else:
            raise ValueError("El nombre no puede estar vacío.")

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, nuevo_email: str):
        if "@" in nuevo_email:
            self._email = nuevo_email
        else:
            raise ValueError("Email no válido.")

    def obtener_detalles(self) -> str:
        """Retorna la información básica del usuario."""
        return f"[{self._id_usuario}] {self._nombre} - {self._email}"

    def __str__(self) -> str:
        return self.obtener_detalles()