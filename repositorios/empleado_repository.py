from typing import List, Optional
from repositorios.repositorio_base import RepositorioBase
from modelos.empleado import Empleado
from modelos.gerente import Gerente

# Clase que representa un repositorio para manejar operaciones CRUD de empleados
# en la base de datos, incluyendo la gestión de gerentes.

class EmpleadoRepository(RepositorioBase):

    def crear(self, empleado: Empleado) -> Empleado:
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            # 1. Insertar correo cifrado en la tabla base usuarios
            cursor.execute(
                "INSERT INTO usuarios (nombre, email) VALUES (?, ?)",
                (empleado.nombre, empleado.obtener_email_cifrado())
            )
            id_u = cursor.lastrowid
            empleado._id_usuario = id_u

            # 2. Insertar en tabla empleados
            cursor.execute(
                "INSERT INTO empleados (id_usuario, cargo, tarifa_hora) VALUES (?, ?, ?)",
                (id_u, empleado.cargo, empleado.tarifa_hora)
            )

            # 3. Si es un Gerente, insertar también en gerentes
            if isinstance(empleado, Gerente):
                cursor.execute(
                    "INSERT INTO gerentes (id_usuario, bono_liderazgo) VALUES (?, ?)",
                    (id_u, empleado.bono_liderazgo)
                )

            conn.commit()
        return empleado

    def obtener_por_id(self, id_usuario: int) -> Optional[Empleado]:
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id_usuario, u.nombre, u.email, e.cargo, e.tarifa_hora, g.bono_liderazgo
                FROM usuarios u
                JOIN empleados e ON u.id_usuario = e.id_usuario
                LEFT JOIN gerentes g ON u.id_usuario = g.id_usuario
                WHERE u.id_usuario = ?
            """, (id_usuario,))
            row = cursor.fetchone()
            if row:
                if row["bono_liderazgo"] is not None:
                    return Gerente(row["id_usuario"], row["nombre"], row["email"], row["tarifa_hora"], row["bono_liderazgo"])
                return Empleado(row["id_usuario"], row["nombre"], row["email"], row["cargo"], row["tarifa_hora"])
        return None

    def obtener_todos(self) -> List[Empleado]:
        empleados = []
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id_usuario, u.nombre, u.email, e.cargo, e.tarifa_hora, g.bono_liderazgo
                FROM usuarios u
                JOIN empleados e ON u.id_usuario = e.id_usuario
                LEFT JOIN gerentes g ON u.id_usuario = g.id_usuario
            """)
            rows = cursor.fetchall()
            for row in rows:
                if row["bono_liderazgo"] is not None:
                    emp = Gerente(row["id_usuario"], row["nombre"], row["email"], row["tarifa_hora"], row["bono_liderazgo"])
                else:
                    emp = Empleado(row["id_usuario"], row["nombre"], row["email"], row["cargo"], row["tarifa_hora"])
                empleados.append(emp)
        return empleados

    def actualizar(self, empleado: Empleado) -> bool:
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET nombre = ?, email = ? WHERE id_usuario = ?",
                           (empleado.nombre, empleado.obtener_email_cifrado(), empleado.id_usuario))
            cursor.execute("UPDATE empleados SET cargo = ?, tarifa_hora = ? WHERE id_usuario = ?",
                           (empleado.cargo, empleado.tarifa_hora, empleado.id_usuario))
            if isinstance(empleado, Gerente):
                cursor.execute("UPDATE gerentes SET bono_liderazgo = ? WHERE id_usuario = ?",
                               (empleado.bono_liderazgo, empleado.id_usuario))
            conn.commit()
            return True

    def eliminar(self, id_usuario: int) -> bool:
        with self.db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (id_usuario,))
            conn.commit()
            return cursor.rowcount > 0