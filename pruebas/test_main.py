import unittest
from unittest.mock import patch

import main
from modelos import Departamento, Gerente, Proyecto


class TestMenuDepartamentos(unittest.TestCase):

    def setUp(self):
        self.departamentos_originales = main.departamentos
        main.departamentos = [Departamento(1, "RRHH")]

    def tearDown(self):
        main.departamentos = self.departamentos_originales

    def test_seleccionar_departamento_existente(self):
        with patch("builtins.input", return_value="1"):
            nombre = main.solicitar_nombre_departamento()

        self.assertIsNone(nombre)

    def test_rechaza_nombre_vacio_y_duplicado(self):
        respuestas = iter(["0", "", "rrhh", "Finanzas"])
        with patch("builtins.input", side_effect=respuestas):
            nombre = main.solicitar_nombre_departamento()

        self.assertEqual(nombre, "Finanzas")

    def test_reintenta_correo_invalido(self):
        empleados_originales = main.empleados
        secuencia_original = main.id_usuario_seq
        main.empleados = []
        empleados_creados = main.empleados
        main.id_usuario_seq = 1
        respuestas = iter([
            "1", "Ana Torres", "correo-invalido", "ana@ecotech.com",
            "25", "Analista"
        ])
        try:
            with patch("builtins.input", side_effect=respuestas), patch.object(main, "auto_guardar"):
                main.registrar_empleado_o_gerente()
        finally:
            main.empleados = empleados_originales
            main.id_usuario_seq = secuencia_original

        self.assertEqual(len(empleados_creados), 1)
        self.assertEqual(empleados_creados[0].email, "ana@ecotech.com")

    def test_modifica_proyecto(self):
        proyectos_originales = main.proyectos
        main.proyectos = [Proyecto(1, "Inicial", 1000)]
        try:
            respuestas = iter(["3", "1", "Actualizado", "2000", "En Progreso"])
            with patch("builtins.input", side_effect=respuestas), patch.object(main, "auto_guardar"):
                main.modificar_datos()
            self.assertEqual(main.proyectos[0].nombre, "Actualizado")
            self.assertEqual(main.proyectos[0].presupuesto, 2000)
            self.assertEqual(main.proyectos[0].estado, "En Progreso")
        finally:
            main.proyectos = proyectos_originales

    def test_elimina_departamento_con_confirmacion(self):
        departamentos_originales = main.departamentos
        main.departamentos = [Departamento(1, "Temporal")]
        try:
            respuestas = iter(["2", "1", "s"])
            with patch("builtins.input", side_effect=respuestas), patch.object(main, "auto_guardar"):
                main.eliminar_datos()
            self.assertEqual(main.departamentos, [])
        finally:
            main.departamentos = departamentos_originales

    def test_repite_confirmacion_si_la_respuesta_no_es_s_o_n(self):
        respuestas = iter(["x", "n"])
        with patch("builtins.input", side_effect=respuestas):
            confirmacion = main.solicitar_confirmacion("¿Continuar?")

        self.assertEqual(confirmacion, "n")

    def test_crear_departamento_repite_confirmacion_invalida(self):
        departamentos_originales = main.departamentos
        empleados_originales = main.empleados
        secuencia_original = main.id_depto_seq
        main.departamentos = []
        main.empleados = [Gerente(1, "Carlos Ruiz", "carlos@ecotech.com", 40, 500)]
        main.id_depto_seq = 1
        try:
            respuestas = iter(["Ventas", "x", "n"])
            with patch("builtins.input", side_effect=respuestas), patch.object(main, "auto_guardar"):
                main.crear_departamento()
            self.assertEqual(len(main.departamentos), 1)
            self.assertIsNone(main.departamentos[0].gerente)
        finally:
            main.departamentos = departamentos_originales
            main.empleados = empleados_originales
            main.id_depto_seq = secuencia_original

    def test_eliminar_departamento_repite_confirmacion_invalida(self):
        departamentos_originales = main.departamentos
        main.departamentos = [Departamento(3, "qq")]
        try:
            respuestas = iter(["2", "1", "x", "n"])
            with patch("builtins.input", side_effect=respuestas), patch.object(main, "auto_guardar"):
                main.eliminar_datos()
            self.assertEqual(len(main.departamentos), 1)
        finally:
            main.departamentos = departamentos_originales


if __name__ == "__main__":
    unittest.main()