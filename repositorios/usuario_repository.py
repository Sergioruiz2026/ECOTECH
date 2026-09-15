from typing import List, Optional
from repositorios.repositorio_base import RepositorioBase
from modelos.usuario import Usuario

# Clase que representa un repositorio para manejar operaciones CRUD de usuarios
# en la base de datos.

class UsuarioRepository(RepositorioBase):

    def crear(self, usuario: Usuario) -> Usuario:
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            
            # Se usa obtener_email_cifrado() para guardar la versión cifrada antes del @
            
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, rol) VALUES (?, ?, ?)",
                (usuario.nombre, usuario.obtener_email_cifrado(), usuario.rol)
            )
            usuario._id_usuario = cursor.lastrowid
            conn.commit()
        return usuario

    def obtener_por_id(self, id_usuario: int) -> Optional[Usuario]:
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id_usuario = ?", (id_usuario,))
            row = cursor.fetchone()
            if row:
                return Usuario(row["id_usuario"], row["nombre"], row["email"], row["rol"], row["password_hash"])
        return None

    def obtener_todos(self) -> List[Usuario]:
        usuarios = []
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            rows = cursor.fetchall()
            for row in rows:
                usuarios.append(Usuario(row["id_usuario"], row["nombre"], row["email"], row["rol"], row["password_hash"]))
        return usuarios

    def actualizar(self, usuario: Usuario) -> bool:
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            # Al actualizar también nos aseguramos de guardar la versión cifrada
            cursor.execute(
                "UPDATE usuarios SET nombre = ?, email = ?, rol = ?, password_hash = ? WHERE id_usuario = ?",
                (usuario.nombre, usuario.obtener_email_cifrado(), usuario.rol, usuario.password_hash, usuario.id_usuario)
            )
            conn.commit()
            return cursor.rowcount > 0

    def eliminar(self, id_usuario: int) -> bool:
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (id_usuario,))
            conn.commit()
            return cursor.rowcount > 0

    def contar(self) -> int:
        with self.db.obtener_conexion() as conn:
            return conn.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]

    def contar_admins(self) -> int:
        with self.db.obtener_conexion() as conn:
            return conn.execute("SELECT COUNT(*) FROM usuarios WHERE rol = 'admin'").fetchone()[0]

    def actualizar_password(self, id_usuario: int, password_hash: str) -> bool:
        with self.db.obtener_conexion() as conn:
            cursor = conn.execute(
                "UPDATE usuarios SET password_hash = ? WHERE id_usuario = ?",
                (password_hash, id_usuario)
            )
            conn.commit()
            return cursor.rowcount > 0