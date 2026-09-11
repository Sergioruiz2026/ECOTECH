#Maneja los proyectos de ECOTECH

from typing import List, Optional
from repositorios.repositorio_base import RepositorioBase
from modelos.proyecto import Proyecto


class ProyectoRepository(RepositorioBase):

    def crear(self, proyecto: Proyecto) -> Proyecto:
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO proyectos (nombre, presupuesto, estado) VALUES (?, ?, ?)",
                (proyecto.nombre, proyecto.presupuesto, proyecto.estado)
            )
            proyecto._id_proyecto = cursor.lastrowid
            conn.commit()
        return proyecto

    def obtener_por_id(self, id_proyecto: int) -> Optional[Proyecto]:
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM proyectos WHERE id_proyecto = ?", (id_proyecto,))
            row = cursor.fetchone()
            if row:
                return Proyecto(row["id_proyecto"], row["nombre"], row["presupuesto"], row["estado"])
        return None

    def obtener_todos(self) -> List[Proyecto]:
        proyectos = []
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM proyectos")
            rows = cursor.fetchall()
            for row in rows:
                proyectos.append(Proyecto(row["id_proyecto"], row["nombre"], row["presupuesto"], row["estado"]))
        return proyectos

    def actualizar(self, proyecto: Proyecto) -> bool:
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE proyectos SET nombre = ?, presupuesto = ?, estado = ? WHERE id_proyecto = ?",
                (proyecto.nombre, proyecto.presupuesto, proyecto.estado, proyecto.id_proyecto)
            )
            conn.commit()
            return cursor.rowcount > 0

    def eliminar(self, id_proyecto: int) -> bool:
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM proyectos WHERE id_proyecto = ?", (id_proyecto,))
            conn.commit()
            return cursor.rowcount > 0