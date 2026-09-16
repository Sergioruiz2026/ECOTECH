#Maneja los proyectos de ECOTECH

import sqlite3
from typing import List
from modelos.proyecto import Proyecto
from repositorios.repositorio_base import RepositorioBase
from database.database import Database

class ProyectoRepository(RepositorioBase):
    def __init__(self, db: Database = None):
        super().__init__(db or Database())

    def crear(self, proyecto: Proyecto) -> Proyecto:
        self.guardar(proyecto)
        return proyecto

    def obtener_todos(self) -> List[Proyecto]:
        with self.db.contexto_conexion() as conexion:
            filas = conexion.execute(
                "SELECT id_proyecto, nombre, presupuesto, estado FROM proyectos ORDER BY id_proyecto"
            ).fetchall()
        return [Proyecto(row[0], row[1], row[2], row[3]) for row in filas]

    def guardar(self, proyecto: Proyecto) -> bool:
        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO proyectos (nombre, presupuesto, estado) VALUES (?, ?, ?)",
                (proyecto.nombre, proyecto.presupuesto, proyecto.estado)
            )
            proyecto._id_proyecto = cursor.lastrowid
            conexion.commit()
            return True
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"Error al guardar proyecto: {e}")
            return False
        finally:
            conexion.close()

    def actualizar(self, proyecto: Proyecto) -> bool:
        """Actualiza los datos de un proyecto existente."""
        if not proyecto.id_proyecto:
            print("Error: El proyecto no tiene id_proyecto asignado.")
            return False

        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "UPDATE proyectos SET nombre = ?, presupuesto = ?, estado = ? WHERE id_proyecto = ?",
                (proyecto.nombre, proyecto.presupuesto, proyecto.estado, proyecto.id_proyecto)
            )
            conexion.commit()
            return True
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"Error al actualizar proyecto: {e}")
            return False
        finally:
            conexion.close()

    def eliminar(self, id_proyecto: int) -> bool:
        """Elimina un proyecto por su ID."""
        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM proyectos WHERE id_proyecto = ?", (id_proyecto,))
            conexion.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"Error al eliminar proyecto: {e}")
            return False
        finally:
            conexion.close()

    def obtener_por_id(self, id_proyecto: int) -> Proyecto | None:
        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id_proyecto, nombre, presupuesto, estado FROM proyectos WHERE id_proyecto = ?",
            (id_proyecto,)
        )
        row = cursor.fetchone()
        conexion.close()

        if row:
            return Proyecto(row[0], row[1], row[2], row[3])
        return None