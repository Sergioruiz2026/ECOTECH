import re
import hashlib

# Clase que representa un usuario con validación de correo electrónico
# y cifrado de la parte local del correo.

class Usuario:
    # Expresión regular para validar formato estándar de e-mail
    PATRON_EMAIL = re.compile(
        r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
        r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
        r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
    )
    PATRON_HASH_EMAIL = re.compile(r"^[0-9a-f]{16}$")

    def __init__(self, id_usuario: int, nombre: str, email: str):
        self._id_usuario = id_usuario
        self.nombre = nombre
        self.email = email  

    @property
    def id_usuario(self) -> int:
        return self._id_usuario

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
        if not self.PATRON_EMAIL.fullmatch(valor):
            raise ValueError(f"El correo electrónico '{valor}' no es válido. Debe tener un formato correcto (ej: usuario@dominio.com).")
        self._email = valor

    def obtener_email_cifrado(self) -> str:
        
     #Retorna el correo con la parte antes del @ cifrada mediante SHA-256 
     #para almacenamiento seguro en la base de datos.
      
        partes = self._email.split("@")
        if len(partes) != 2:
            return self._email

        usuario_local, dominio = partes[0], partes[1]
        if self.PATRON_HASH_EMAIL.fullmatch(usuario_local):
            return self._email
        
        # Generar hash SHA-256 de la parte previa al @
        
        hash_local = hashlib.sha256(usuario_local.encode("utf-8")).hexdigest()[:16] # Guardamos los primeros 16 caracteres
        return f"{hash_local}@{dominio}"

    def obtener_detalles(self) -> str:
        return f"ID: {self._id_usuario} | Nombre: {self._nombre} | Email: {self._email}"

    def __str__(self) -> str:
        return self.obtener_detalles()