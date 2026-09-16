#Utilizaremos SQLite3 para gestionar la persistencia en una base de datos relacional,
#creando las tablas necesarias para todos los modelos del proyecto.

import sqlite3
import os
from contextlib import closing
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "ecotech.db")


class _ConexionSQLite:
    def __init__(self, conexion: sqlite3.Connection):
        self._conexion = conexion

    def __enter__(self):
        self._conexion.__enter__()
        return self._conexion

    def __exit__(self, tipo, valor, traceback):
        try:
            return self._conexion.__exit__(tipo, valor, traceback)
        finally:
            self._conexion.close()

    def close(self):
        self._conexion.close()

    def __getattr__(self, nombre):
        return getattr(self._conexion, nombre)


class Database:
    
    #Clase encargada de gestionar la conexión y creación de tablas en SQLite.

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def obtener_conexion(self) -> sqlite3.Connection:
        """Crea y retorna una conexión a la base de datos."""
        conn = sqlite3.connect(self.db_path)
        # Habilitar el soporte de claves foráneas en SQLite
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
        return _ConexionSQLite(conn)

    def inicializar_tablas(self):
        """Crea las tablas principales del sistema si aún no existen."""
        with closing(self.obtener_conexion()) as conn:
            cursor = conn.cursor()

            # Tabla Usuarios (Clase Base)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    rol TEXT NOT NULL DEFAULT 'usuario' CHECK(rol IN ('usuario', 'admin')),
                    password_hash TEXT
                );
            """)

            columnas_usuario = [fila[1] for fila in cursor.execute("PRAGMA table_info(usuarios)")]
            if "rol" not in columnas_usuario:
                cursor.execute(
                    "ALTER TABLE usuarios ADD COLUMN rol TEXT NOT NULL DEFAULT 'usuario' "
                    "CHECK(rol IN ('usuario', 'admin'))"
                )
            if "password_hash" not in columnas_usuario:
                cursor.execute("ALTER TABLE usuarios ADD COLUMN password_hash TEXT")
            cursor.execute("""
                UPDATE usuarios
                SET rol = 'admin'
                WHERE id_usuario = (SELECT MIN(id_usuario) FROM usuarios)
                  AND NOT EXISTS (SELECT 1 FROM usuarios WHERE rol = 'admin')
            """)

            columnas_empleado = [
                fila[1] for fila in cursor.execute("PRAGMA table_info(empleados)")
            ]
            if "id_usuario" in columnas_empleado and "id_empleado" not in columnas_empleado:
                conn.commit()
                self._migrar_tablas_empleados(conn)

            # Tabla Empleados (asociación opcional con Usuario)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleados (
                    id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    email TEXT NOT NULL,
                    cargo TEXT NOT NULL,
                    tarifa_hora REAL NOT NULL CHECK(tarifa_hora > 0),
                    id_usuario INTEGER UNIQUE NULL,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
                );
            """)

            # Tabla Gerentes (especialización de Empleado)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gerentes (
                    id_empleado INTEGER PRIMARY KEY,
                    bono_liderazgo REAL DEFAULT 1.0 CHECK(bono_liderazgo > 0),
                    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE CASCADE
                );
            """)

            # Tabla Departamentos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departamentos (
                    id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL
                );
            """)

            columnas_departamento = [
                fila[1] for fila in cursor.execute("PRAGMA table_info(departamentos)")
            ]
            if "id_gerente" in columnas_departamento:
                self._migrar_departamentos_sin_gerente(conn)

            # Relación Muchos a Muchos / Asignación: Empleado - Departamento
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departamento_empleados (
                    id_departamento INTEGER NOT NULL,
                    id_empleado INTEGER NOT NULL,
                    PRIMARY KEY (id_departamento, id_empleado),
                    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento) ON DELETE CASCADE,
                    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE CASCADE
                );
            """)

            # Tabla Proyectos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS proyectos (
                    id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    presupuesto REAL NOT NULL CHECK(presupuesto >= 0),
                    estado TEXT DEFAULT 'Planificación'
                );
            """)

            # Tabla Registros de Tiempo
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS registros_tiempo (
                    id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_empleado INTEGER NOT NULL,
                    id_proyecto INTEGER NOT NULL,
                    horas_trabajadas REAL NOT NULL CHECK(horas_trabajadas > 0),
                    fecha TEXT NOT NULL,
                    descripcion TEXT,
                    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE CASCADE,
                    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto) ON DELETE CASCADE
                );
            """)

            conn.commit()
            print("Base de datos inicializada correctamente.")

    def _migrar_tablas_empleados(self, conn: sqlite3.Connection):
        """Migra el esquema heredado de empleados con PK compartida."""
        conn.execute("PRAGMA foreign_keys = OFF")

        tablas_anteriores = (
            "registros_tiempo",
            "departamento_empleados",
            "departamentos",
            "gerentes",
            "empleados",
        )
        for tabla in tablas_anteriores:
            conn.execute(f"ALTER TABLE {tabla} RENAME TO {tabla}_legacy")

        conn.execute("""
            CREATE TABLE empleados (
                id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL,
                cargo TEXT NOT NULL,
                tarifa_hora REAL NOT NULL CHECK(tarifa_hora > 0),
                id_usuario INTEGER UNIQUE NULL,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
            )
        """)
        conn.execute("""
            INSERT INTO empleados (id_empleado, nombre, email, cargo, tarifa_hora, id_usuario)
            SELECT e.id_usuario, u.nombre, u.email, e.cargo, e.tarifa_hora, e.id_usuario
            FROM empleados_legacy e
            JOIN usuarios u ON u.id_usuario = e.id_usuario
        """)

        conn.execute("""
            CREATE TABLE gerentes (
                id_empleado INTEGER PRIMARY KEY,
                bono_liderazgo REAL DEFAULT 1.0 CHECK(bono_liderazgo > 0),
                FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE CASCADE
            )
        """)
        conn.execute("""
            INSERT INTO gerentes (id_empleado, bono_liderazgo)
            SELECT id_usuario, bono_liderazgo FROM gerentes_legacy
        """)

        conn.execute("""
            CREATE TABLE departamentos (
                id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL
            )
        """)
        conn.execute("""
            INSERT INTO departamentos (id_departamento, nombre)
            SELECT id_departamento, nombre FROM departamentos_legacy
        """)

        conn.execute("""
            CREATE TABLE departamento_empleados (
                id_departamento INTEGER NOT NULL,
                id_empleado INTEGER NOT NULL,
                PRIMARY KEY (id_departamento, id_empleado),
                FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento) ON DELETE CASCADE,
                FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE CASCADE
            )
        """)
        conn.execute("""
            INSERT INTO departamento_empleados (id_departamento, id_empleado)
            SELECT id_departamento, id_empleado FROM departamento_empleados_legacy
        """)
        conn.execute("""
            INSERT OR IGNORE INTO departamento_empleados (id_departamento, id_empleado)
            SELECT id_departamento, id_gerente
            FROM departamentos_legacy
            WHERE id_gerente IS NOT NULL
        """)

        conn.execute("""
            CREATE TABLE registros_tiempo (
                id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
                id_empleado INTEGER NOT NULL,
                id_proyecto INTEGER NOT NULL,
                horas_trabajadas REAL NOT NULL CHECK(horas_trabajadas > 0),
                fecha TEXT NOT NULL,
                descripcion TEXT,
                FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE CASCADE,
                FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto) ON DELETE CASCADE
            )
        """)
        conn.execute("""
            INSERT INTO registros_tiempo
                (id_registro, id_empleado, id_proyecto, horas_trabajadas, fecha, descripcion)
            SELECT id_registro, id_empleado, id_proyecto, horas_trabajadas, fecha, descripcion
            FROM registros_tiempo_legacy
        """)

        for tabla in tablas_anteriores:
            conn.execute(f"DROP TABLE {tabla}_legacy")

        conn.commit()
        conn.execute("PRAGMA foreign_keys = ON")

    def _migrar_departamentos_sin_gerente(self, conn: sqlite3.Connection):
        """Elimina id_gerente conservando sus asociaciones como empleados."""
        conn.execute("PRAGMA foreign_keys = OFF")

        conn.execute("ALTER TABLE departamentos RENAME TO departamentos_legacy")
        conn.execute(
            "ALTER TABLE departamento_empleados "
            "RENAME TO departamento_empleados_legacy"
        )

        conn.execute("""
            CREATE TABLE departamentos (
                id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL
            )
        """)
        conn.execute("""
            INSERT INTO departamentos (id_departamento, nombre)
            SELECT id_departamento, nombre FROM departamentos_legacy
        """)

        conn.execute("""
            CREATE TABLE departamento_empleados (
                id_departamento INTEGER NOT NULL,
                id_empleado INTEGER NOT NULL,
                PRIMARY KEY (id_departamento, id_empleado),
                FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
                    ON DELETE CASCADE,
                FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
                    ON DELETE CASCADE
            )
        """)
        conn.execute("""
            INSERT INTO departamento_empleados (id_departamento, id_empleado)
            SELECT id_departamento, id_empleado
            FROM departamento_empleados_legacy
        """)
        conn.execute("""
            INSERT OR IGNORE INTO departamento_empleados (id_departamento, id_empleado)
            SELECT id_departamento, id_gerente
            FROM departamentos_legacy
            WHERE id_gerente IS NOT NULL
        """)

        conn.execute("DROP TABLE departamento_empleados_legacy")
        conn.execute("DROP TABLE departamentos_legacy")
        conn.commit()
        conn.execute("PRAGMA foreign_keys = ON")


if __name__ == "__main__":
    db = Database()
    db.inicializar_tablas()