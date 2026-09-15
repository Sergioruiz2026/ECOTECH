import sqlite3
from entidades.empleado import Empleado
from repositorios.repositorio_base import RepositorioBase

class EmpleadoRepository(RepositorioBase):
    def __init__(self, db_path: str = "ecotech.db"):
        super().__init__(db_path)

    def guardar(self, empleado: Empleado) -> bool:
        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        try:
            # 1. Insertar en tabla usuarios
            cursor.execute(
                "INSERT INTO usuarios (nombre, email) VALUES (?, ?)",
                (empleado.nombre, empleado.obtener_email_cifrado())
            )
            id_usuario = cursor.lastrowid
            empleado.id_usuario = id_usuario

            # 2. Insertar en tabla empleados
            cursor.execute(
                "INSERT INTO empleados (id_usuario, cargo, tarifa_hora) VALUES (?, ?, ?)",
                (id_usuario, empleado.cargo, empleado.tarifa_hora)
            )
            conexion.commit()
            return True
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"Error al guardar empleado: {e}")
            return False
        finally:
            conexion.close()

    def actualizar(self, empleado: Empleado) -> bool:
        """Actualiza los datos del empleado y su usuario base."""
        if not empleado.id_usuario:
            print("Error: El empleado no tiene id_usuario asignado.")
            return False

        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        try:
            # Actualizar datos de usuario
            cursor.execute(
                "UPDATE usuarios SET nombre = ?, email = ? WHERE id_usuario = ?",
                (empleado.nombre, empleado.obtener_email_cifrado(), empleado.id_usuario)
            )
            # Actualizar datos de empleado
            cursor.execute(
                "UPDATE empleados SET cargo = ?, tarifa_hora = ? WHERE id_usuario = ?",
                (empleado.cargo, empleado.tarifa_hora, empleado.id_usuario)
            )
            conexion.commit()
            return True
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"Error al actualizar empleado: {e}")
            return False
        finally:
            conexion.close()

    def eliminar(self, id_usuario: int) -> bool:
        """Elimina un empleado por su ID. La cascada elimina el registro en usuarios y empleados."""
        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (id_usuario,))
            conexion.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"Error al eliminar empleado: {e}")
            return False
        finally:
            conexion.close()

    def obtener_por_id(self, id_usuario: int) -> Empleado | None:
        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            SELECT u.id_usuario, u.nombre, u.email, e.cargo, e.tarifa_hora
            FROM usuarios u
            JOIN empleados e ON u.id_usuario = e.id_usuario
            WHERE u.id_usuario = ?
        ''', (id_usuario,))
        row = cursor.fetchone()
        conexion.close()

        if row:
            emp = Empleado(nombre=row[1], email=row[2], cargo=row[3], tarifa_hora=row[4])
            emp.id_usuario = row[0]
            return emp
        return None