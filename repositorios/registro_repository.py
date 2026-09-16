#Asocia empleados, proyectos y horas trabajadas 
#registrando el tiempo y calculando costos laborales.

from typing import List, Optional
from repositorios.repositorio_base import RepositorioBase
from repositorios.empleado_repository import EmpleadoRepository
from repositorios.proyecto_repository import ProyectoRepository
from modelos.registro_tiempo import RegistroTiempo


class RegistroTiempoRepository(RepositorioBase):

    def __init__(self, db):
        super().__init__(db)
        self.emp_repo = EmpleadoRepository(db)
        self.proy_repo = ProyectoRepository(db)

    def crear(self, registro: RegistroTiempo) -> RegistroTiempo:
        with self.db.contexto_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO registros_tiempo (id_empleado, id_proyecto, horas_trabajadas, fecha, descripcion)
                VALUES (?, ?, ?, ?, ?)
            """, (
                registro.empleado.id_empleado,
                registro.proyecto.id_proyecto,
                registro.horas_trabajadas,
                registro._fecha,
                registro._descripcion
            ))
            registro._id_registro = cursor.lastrowid
            conn.commit()
        return registro

    def obtener_por_id(self, id_registro: int) -> Optional[RegistroTiempo]:
        with self.db.contexto_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM registros_tiempo WHERE id_registro = ?", (id_registro,))
            row = cursor.fetchone()
            if row:
                emp = self.emp_repo.obtener_por_id(row["id_empleado"])
                proy = self.proy_repo.obtener_por_id(row["id_proyecto"])
                if emp and proy:
                    return RegistroTiempo(
                        row["id_registro"], emp, proy, row["horas_trabajadas"], row["fecha"], row["descripcion"]
                    )
        return None

    def obtener_todos(self) -> List[RegistroTiempo]:
        registros = []
        with self.db.contexto_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_registro FROM registros_tiempo")
            rows = cursor.fetchall()
            for row in rows:
                reg = self.obtener_por_id(row["id_registro"])
                if reg:
                    registros.append(reg)
        return registros

    def actualizar(self, registro: RegistroTiempo) -> bool:
        with self.db.contexto_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE registros_tiempo 
                SET id_empleado = ?, id_proyecto = ?, horas_trabajadas = ?, fecha = ?, descripcion = ?
                WHERE id_registro = ?
            """, (
                registro.empleado.id_empleado,
                registro.proyecto.id_proyecto,
                registro.horas_trabajadas,
                registro._fecha,
                registro._descripcion,
                registro.id_registro
            ))
            conn.commit()
            return cursor.rowcount > 0

    def eliminar(self, id_registro: int) -> bool:
        with self.db.contexto_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM registros_tiempo WHERE id_registro = ?", (id_registro,))
            conn.commit()
            return cursor.rowcount > 0