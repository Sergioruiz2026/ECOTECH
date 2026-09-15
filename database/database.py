#Utilizaremos SQLite3 para gestionar la persistencia en una base de datos relacional,
#creando las tablas necesarias para todos los modelos del proyecto.

import sqlite3
import os
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "ecotech.db")


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
        return conn

    def inicializar_tablas(self):
        """Crea las tablas principales del sistema si aún no existen."""
        with self.obtener_conexion() as conn:
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

            # Tabla Empleados (Hereda atributos de Usuario)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleados (
                    id_usuario INTEGER PRIMARY KEY,
                    cargo TEXT NOT NULL,
                    tarifa_hora REAL NOT NULL CHECK(tarifa_hora > 0),
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
                );
            """)

            # Tabla Gerentes (Hereda de Empleado)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gerentes (
                    id_usuario INTEGER PRIMARY KEY,
                    bono_liderazgo REAL DEFAULT 1.0 CHECK(bono_liderazgo > 0),
                    FOREIGN KEY (id_usuario) REFERENCES empleados(id_usuario) ON DELETE CASCADE
                );
            """)

            # Tabla Departamentos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departamentos (
                    id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    id_gerente INTEGER NULL,
                    FOREIGN KEY (id_gerente) REFERENCES gerentes(id_usuario) ON DELETE SET NULL
                );
            """)

            # Relación Muchos a Muchos / Asignación: Empleado - Departamento
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departamento_empleados (
                    id_departamento INTEGER NOT NULL,
                    id_empleado INTEGER NOT NULL,
                    PRIMARY KEY (id_departamento, id_empleado),
                    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento) ON DELETE CASCADE,
                    FOREIGN KEY (id_empleado) REFERENCES empleados(id_usuario) ON DELETE CASCADE
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
                    FOREIGN KEY (id_empleado) REFERENCES empleados(id_usuario) ON DELETE CASCADE,
                    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto) ON DELETE CASCADE
                );
            """)

            conn.commit()
            print("Base de datos inicializada correctamente.")


if __name__ == "__main__":
    db = Database()
    db.inicializar_tablas()