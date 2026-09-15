import re
import hashlib
import hmac
import secrets

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

    ROLES_VALIDOS = {"usuario", "admin"}

    def __init__(self, id_usuario: int, nombre: str, email: str, rol: str = "usuario", password_hash: str = None):
        self._id_usuario = id_usuario
        self.nombre = nombre
        self.email = email  
        self.rol = rol
        self.password_hash = password_hash

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

    @property
    def rol(self) -> str:
        return self._rol

    @rol.setter
    def rol(self, valor: str):
        valor = str(valor).strip().lower()
        if valor not in self.ROLES_VALIDOS:
            raise ValueError("El rol debe ser 'usuario' o 'admin'.")
        self._rol = valor

    def establecer_contraseña(self, contraseña: str):
        if not isinstance(contraseña, str) or len(contraseña) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        sal = secrets.token_bytes(16)
        resumen = hashlib.pbkdf2_hmac(
            "sha256", contraseña.encode("utf-8"), sal, 300_000
        )
        self.password_hash = f"{sal.hex()}${resumen.hex()}"

    def verificar_contraseña(self, contraseña: str) -> bool:
        if not self.password_hash or "$" not in self.password_hash:
            return False
        sal_hex, resumen_hex = self.password_hash.split("$", 1)
        try:
            resumen = hashlib.pbkdf2_hmac(
                "sha256", contraseña.encode("utf-8"), bytes.fromhex(sal_hex), 300_000
            )
            return hmac.compare_digest(resumen.hex(), resumen_hex)
        except ValueError:
            return False

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