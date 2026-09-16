#Maneja los departamentos y su relación de empleados asociados

import sqlite3
from typing import List
from modelos.departamento import Departamento
from repositorios.repositorio_base import RepositorioBase
from repositorios.empleado_repository import EmpleadoRepository
from database.database import Database

class DepartamentoRepository(RepositorioBase):
    def __init__(self, db: Database = None):
        super().__init__(db or Database())

    def crear(self, departamento: Departamento) -> Departamento:
        self.guardar(departamento)
        return departamento

    def obtener_todos(self) -> List[Departamento]:
        with self.obtener_conexion() as conexion:
            filas = conexion.execute(
                "SELECT id_departamento, nombre FROM departamentos ORDER BY id_departamento"
            ).fetchall()
        return [self._reconstruir_departamento(row) for row in filas]

    def guardar(self, departamento: Departamento) -> bool:
        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO departamentos (nombre) VALUES (?)",
                (departamento.nombre,)
            )
            departamento._id_departamento = cursor.lastrowid
            self._guardar_empleados(cursor, departamento)
            conexion.commit()
            return True
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"Error al guardar departamento: {e}")
            return False
        finally:
            conexion.close()

    def actualizar(self, departamento: Departamento) -> bool:
        """Actualiza el nombre y los empleados del departamento."""
        if not departamento.id_departamento:
            print("Error: El departamento no tiene id_departamento asignado.")
            return False

        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "UPDATE departamentos SET nombre = ? WHERE id_departamento = ?",
                (
                    departamento.nombre,
                    departamento.id_departamento,
                )
            )
            actualizado = cursor.rowcount > 0
            cursor.execute(
                "DELETE FROM departamento_empleados WHERE id_departamento = ?",
                (departamento.id_departamento,),
            )
            self._guardar_empleados(cursor, departamento)
            conexion.commit()
            return actualizado
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"Error al actualizar departamento: {e}")
            return False
        finally:
            conexion.close()

    def eliminar(self, id_departamento: int) -> bool:
        """Elimina un departamento por su ID."""
        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM departamentos WHERE id_departamento = ?", (id_departamento,))
            conexion.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"Error al eliminar departamento: {e}")
            return False
        finally:
            conexion.close()

    def obtener_por_id(self, id_departamento: int) -> Departamento | None:
        with self.obtener_conexion() as conexion:
            row = conexion.execute(
                "SELECT id_departamento, nombre "
                "FROM departamentos WHERE id_departamento = ?",
                (id_departamento,),
            ).fetchone()

        if row:
            return self._reconstruir_departamento(row)
        return None

    def agregar_empleado_a_departamento(self, id_departamento: int, id_empleado: int) -> bool:
        """Asocia un empleado existente con un departamento."""
        conexion = self.obtener_conexion()
        try:
            cursor = conexion.execute(
                "INSERT OR IGNORE INTO departamento_empleados "
                "(id_departamento, id_empleado) VALUES (?, ?)",
                (id_departamento, id_empleado),
            )
            conexion.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"Error al agregar empleado al departamento: {e}")
            return False
        finally:
            conexion.close()

    def quitar_empleado_de_departamento(self, id_departamento: int, id_empleado: int) -> bool:
        """Elimina la asociación entre un empleado y un departamento."""
        conexion = self.obtener_conexion()
        try:
            cursor = conexion.execute(
                "DELETE FROM departamento_empleados "
                "WHERE id_departamento = ? AND id_empleado = ?",
                (id_departamento, id_empleado),
            )
            conexion.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"Error al quitar empleado del departamento: {e}")
            return False
        finally:
            conexion.close()

    @staticmethod
    def _guardar_empleados(cursor, departamento: Departamento) -> None:
        cursor.executemany(
            "INSERT INTO departamento_empleados (id_departamento, id_empleado) "
            "VALUES (?, ?)",
            [
                (departamento.id_departamento, empleado.id_empleado)
                for empleado in departamento.empleados
            ],
        )

    def _reconstruir_departamento(self, fila) -> Departamento:
        departamento = Departamento(fila[0], fila[1])

        with self.obtener_conexion() as conexion:
            empleados = conexion.execute(
                "SELECT id_empleado FROM departamento_empleados "
                "WHERE id_departamento = ? ORDER BY id_empleado",
                (fila[0],),
            ).fetchall()

        empleado_repo = EmpleadoRepository(self.db)
        for empleado_row in empleados:
            empleado = empleado_repo.obtener_por_id(empleado_row[0])
            if empleado:
                departamento.agregar_empleado(empleado)
        return departamento
