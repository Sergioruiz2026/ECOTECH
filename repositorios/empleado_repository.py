import sqlite3
from typing import List

from modelos.empleado import Empleado
from modelos.gerente import Gerente
from modelos.usuario import Usuario
from repositorios.repositorio_base import RepositorioBase
from database.database import Database


class EmpleadoRepository(RepositorioBase):
    def __init__(self, db: Database = None):
        super().__init__(db or Database())

    def crear(self, empleado: Empleado) -> Empleado:
        self.guardar(empleado)
        return empleado

    def obtener_todos(self) -> List[Empleado]:
        with self.db.contexto_conexion() as conexion:
            filas = conexion.execute('''
                  SELECT e.id_empleado, e.nombre, e.email, e.cargo, e.tarifa_hora,
                      g.bono_liderazgo,
                       u.id_usuario AS usuario_id, u.nombre AS usuario_nombre,
                       u.email AS usuario_email, u.rol AS usuario_rol,
                       u.password_hash
                FROM empleados e
                LEFT JOIN gerentes g ON g.id_empleado = e.id_empleado
                LEFT JOIN usuarios u ON u.id_usuario = e.id_usuario
                ORDER BY e.id_empleado
            ''').fetchall()
        return [self._construir_empleado(row) for row in filas]

    def guardar(self, empleado: Empleado) -> bool:
        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO empleados "
                "(nombre, email, cargo, tarifa_hora, id_usuario) VALUES (?, ?, ?, ?, ?)",
                (
                    empleado.nombre,
                    empleado.obtener_email_cifrado(),
                    empleado.cargo,
                    empleado.tarifa_hora,
                    empleado.usuario.id_usuario if empleado.usuario else None,
                ),
            )
            empleado._id_empleado = cursor.lastrowid
            if isinstance(empleado, Gerente):
                cursor.execute(
                    "INSERT INTO gerentes (id_empleado, bono_liderazgo) "
                    "VALUES (?, ?)",
                    (empleado.id_empleado, empleado.bono_liderazgo),
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
        """Actualiza la ficha laboral y su asociación opcional."""
        if not empleado.id_empleado:
            print("Error: El empleado no tiene id_empleado asignado.")
            return False

        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "UPDATE empleados SET nombre = ?, email = ?, cargo = ?, "
                "tarifa_hora = ?, id_usuario = ? WHERE id_empleado = ?",
                (
                    empleado.nombre,
                    empleado.obtener_email_cifrado(),
                    empleado.cargo,
                    empleado.tarifa_hora,
                    empleado.usuario.id_usuario if empleado.usuario else None,
                    empleado.id_empleado,
                ),
            )
            conexion.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"Error al actualizar empleado: {e}")
            return False
        finally:
            conexion.close()

    def eliminar(self, id_empleado: int) -> bool:
        """Elimina una ficha laboral sin eliminar la cuenta de usuario."""
        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "DELETE FROM empleados WHERE id_empleado = ?",
                (id_empleado,),
            )
            conexion.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"Error al eliminar empleado: {e}")
            return False
        finally:
            conexion.close()

    def obtener_por_id(self, id_empleado: int) -> Empleado | None:
        with self.db.contexto_conexion() as conexion:
            row = conexion.execute('''
                  SELECT e.id_empleado, e.nombre, e.email, e.cargo, e.tarifa_hora,
                      g.bono_liderazgo,
                       u.id_usuario AS usuario_id, u.nombre AS usuario_nombre,
                       u.email AS usuario_email, u.rol AS usuario_rol,
                       u.password_hash
                FROM empleados e
                LEFT JOIN gerentes g ON g.id_empleado = e.id_empleado
                LEFT JOIN usuarios u ON u.id_usuario = e.id_usuario
                WHERE e.id_empleado = ?
            ''', (id_empleado,)).fetchone()

        if row:
            return self._construir_empleado(row)
        return None

    @staticmethod
    def _construir_empleado(row) -> Empleado:
        usuario = None
        if row[6] is not None:
            usuario = Usuario(row[6], row[7], row[8], row[9], row[10])
        if row[5] is not None:
            return Gerente(row[0], row[1], row[2], row[4], row[5], usuario)
        return Empleado(row[0], row[1], row[2], row[3], row[4], usuario)