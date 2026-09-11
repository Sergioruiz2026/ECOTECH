#Maneja los departamentos y su relación de empleados asociados

from typing import List, Optional
from repositorios.repositorio_base import RepositorioBase
from repositorios.empleado_repository import EmpleadoRepository
from modelos.departamento import Departamento
from modelos.gerente import Gerente


class DepartamentoRepository(RepositorioBase):

    def __init__(self, db):
        super().__init__(db)
        self.emp_repo = EmpleadoRepository(db)

    def crear(self, departamento: Departamento) -> Departamento:
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            id_g = departamento.gerente.id_usuario if departamento.gerente else None
            cursor.execute(
                "INSERT INTO departamentos (nombre, id_gerente) VALUES (?, ?)",
                (departamento.nombre, id_g)
            )
            departamento._id_departamento = cursor.lastrowid

            for emp in departamento.empleados:
                cursor.execute(
                    "INSERT INTO departamento_empleados (id_departamento, id_empleado) VALUES (?, ?)",
                    (departamento.id_departamento, emp.id_usuario)
                )
            conn.commit()
        return departamento

    def obtener_por_id(self, id_departamento: int) -> Optional[Departamento]:
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM departamentos WHERE id_departamento = ?", (id_departamento,))
            row = cursor.fetchone()
            if not row:
                return None

            gerente = self.emp_repo.obtener_por_id(row["id_gerente"]) if row["id_gerente"] else None
            if gerente and not isinstance(gerente, Gerente):
                gerente = None

            depto = Departamento(row["id_departamento"], row["nombre"], gerente)

            # Obtener miembros del departamento
            cursor.execute("SELECT id_empleado FROM departamento_empleados WHERE id_departamento = ?", (id_departamento,))
            emp_rows = cursor.fetchall()
            for emp_row in emp_rows:
                emp = self.emp_repo.obtener_por_id(emp_row["id_empleado"])
                if emp:
                    depto.agregar_empleado(emp)

            return depto

    def obtener_todos(self) -> List[Departamento]:
        deptos = []
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_departamento FROM departamentos")
            rows = cursor.fetchall()
            for row in rows:
                d = self.obtener_por_id(row["id_departamento"])
                if d:
                    deptos.append(d)
        return deptos

    def actualizar(self, departamento: Departamento) -> bool:
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            id_g = departamento.gerente.id_usuario if departamento.gerente else None
            cursor.execute(
                "UPDATE departamentos SET nombre = ?, id_gerente = ? WHERE id_departamento = ?",
                (departamento.nombre, id_g, departamento.id_departamento)
            )
            conn.commit()
            return True

    def eliminar(self, id_departamento: int) -> bool:
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM departamentos WHERE id_departamento = ?", (id_departamento,))
            conn.commit()
            return cursor.rowcount > 0