#Maneja los departamentos y su relación de empleados asociados

import sqlite3
from typing import List
from modelos.departamento import Departamento
from repositorios.repositorio_base import RepositorioBase
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
                "SELECT id_departamento, nombre, id_gerente FROM departamentos ORDER BY id_departamento"
            ).fetchall()
        return [Departamento(row[0], row[1]) for row in filas]

    def guardar(self, departamento: Departamento) -> bool:
        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO departamentos (nombre, id_gerente) VALUES (?, ?)",
                (departamento.nombre, None)
            )
            departamento._id_departamento = cursor.lastrowid
            conexion.commit()
            return True
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"Error al guardar departamento: {e}")
            return False
        finally:
            conexion.close()

    def actualizar(self, departamento: Departamento) -> bool:
        """Actualiza el nombre o gerente asignado al departamento."""
        if not departamento.id_departamento:
            print("Error: El departamento no tiene id_departamento asignado.")
            return False

        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "UPDATE departamentos SET nombre = ?, id_gerente = ? WHERE id_departamento = ?",
                (departamento.nombre, None, departamento.id_departamento)
            )
            conexion.commit()
            return True
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
        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id_departamento, nombre, id_gerente FROM departamentos WHERE id_departamento = ?",
            (id_departamento,)
        )
        row = cursor.fetchone()
        conexion.close()

        if row:
            return Departamento(row[0], row[1])
        return None