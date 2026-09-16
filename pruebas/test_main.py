"""
Pruebas para MenuApp (main.py), adaptadas a la versión actual basada en clase + SQLite.

Estrategia:
- Cada test usa una base de datos SQLite temporal (nunca la real ecotech.db).
- Se simulan las entradas de teclado con unittest.mock.patch sobre builtins.input
  y getpass.getpass.
- Se llama directamente a los métodos de MenuApp, no al bucle del menú.
"""

import os
import unittest
from unittest.mock import patch

from database.database import Database
from main import MenuApp


class BaseTestMenuApp(unittest.TestCase):
    """Clase base: crea una BD temporal distinta para cada test y la borra al final."""

    def setUp(self):
        self.db_path = "test_ecotech_tmp.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.db = Database(self.db_path)
        self.db.inicializar_tablas()

        # MenuApp crea su propia Database() por defecto; se la reemplazamos
        # después de construirla para que use la de prueba.
        self.app = MenuApp()
        self.app.repo_usuario.db = self.db
        self.app.repo_empleado.db = self.db
        self.app.repo_departamento.db = self.db
        self.app.repo_proyecto.db = self.db
        self.app.repo_registro.db = self.db

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)


class TestRegistroUsuario(BaseTestMenuApp):

    @patch("getpass.getpass")
    @patch("builtins.input")
    def test_registrar_usuario_persiste_password(self, mock_input, mock_getpass):
        # Simula: nombre, email, rol=admin (primer usuario)
        mock_input.side_effect = ["Sergio Ruiz", "sergio@ecotech.com", "admin"]
        # Simula: contraseña y confirmación
        mock_getpass.side_effect = ["claveSuperSegura123", "claveSuperSegura123"]

        self.app.registrar_usuario(permitir_admin=True)

        usuarios = self.app.repo_usuario.obtener_todos()
        self.assertEqual(len(usuarios), 1)
        # Este es el bug que corregimos con el prompt 1: el hash debe quedar guardado.
        self.assertIsNotNone(usuarios[0].password_hash)
        self.assertTrue(usuarios[0].verificar_contraseña("claveSuperSegura123"))


class TestDepartamentoConGerente(BaseTestMenuApp):

    def test_departamento_conserva_gerente_y_empleados_al_recargar(self):
        # Creamos un gerente directamente vía repositorio (sin pasar por el menú)
        from modelos.gerente import Gerente
        gerente = Gerente(0, "Carla Jefa", "carla@ecotech.com", tarifa_hora=40.0)
        self.app.repo_empleado.crear(gerente)

        from modelos.departamento import Departamento
        depto = Departamento(0, "TI")
        depto.agregar_empleado(gerente)
        self.app.repo_departamento.crear(depto)

        # Recargamos desde la base de datos, como si fuera otra sesión del programa
        recargado = self.app.repo_departamento.obtener_por_id(depto.id_departamento)

        # Esto es lo que arreglamos con el prompt 2 y el prompt 4:
        self.assertEqual(len(recargado.empleados), 1)
        self.assertIsNotNone(recargado.obtener_gerente())
        self.assertEqual(recargado.obtener_gerente().nombre, "Carla Jefa")


class TestRegistroTiempoValidacionHoras(BaseTestMenuApp):

    def test_rechaza_mas_de_24_horas(self):
        from modelos.empleado import Empleado
        from modelos.proyecto import Proyecto
        from modelos.registro_tiempo import RegistroTiempo

        empleado = Empleado(0, "Ana", "ana@ecotech.com", "Dev", 25.0)
        self.app.repo_empleado.crear(empleado)
        proyecto = Proyecto(0, "Panel Solar", 5000.0)
        self.app.repo_proyecto.crear(proyecto)

        # Esto es lo que arreglamos con el prompt 5: debe lanzar ValueError.
        with self.assertRaises(ValueError):
            RegistroTiempo(0, empleado, proyecto, 30.0)

    def test_acepta_horas_dentro_del_rango(self):
        from modelos.empleado import Empleado
        from modelos.proyecto import Proyecto
        from modelos.registro_tiempo import RegistroTiempo

        empleado = Empleado(0, "Ana", "ana@ecotech.com", "Dev", 25.0)
        proyecto = Proyecto(0, "Panel Solar", 5000.0)
        registro = RegistroTiempo(0, empleado, proyecto, 8.0)
        self.assertEqual(registro.horas_trabajadas, 8.0)


if __name__ == "__main__":
    unittest.main()