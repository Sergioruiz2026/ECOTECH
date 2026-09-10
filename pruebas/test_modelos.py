import unittest
from modelos import Empleado, Gerente, Departamento, Proyecto, RegistroTiempo


class TestModelosEcoTech(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada prueba para preparar datos limpios."""
        self.empleado = Empleado(1, "Ana Gómez", "ana@ecotech.com", "Desarrolladora", 25.0)
        self.gerente = Gerente(2, "Carlos Ruiz", "carlos@ecotech.com", tarifa_hora=40.0, bono_liderazgo=500.0)
        self.proyecto = Proyecto(101, "Instalación Solar", 15000.0)

    def test_creacion_y_validacion_empleado(self):
        """Verifica la creación del empleado y validación de atributos."""
        self.assertEqual(self.empleado.nombre, "Ana Gómez")
        self.assertEqual(self.empleado.tarifa_hora, 25.0)

        # Probar error con tarifa negativa
        with self.assertRaises(ValueError):
            self.empleado.tarifa_hora = -10.0

    def test_herencia_gerente(self):
        """Verifica que Gerente hereda de Empleado y mantiene su comportamiento."""
        self.assertEqual(self.gerente.cargo, "Gerente")
        self.assertEqual(self.gerente.bono_liderazgo, 500.0)

        # Asignar empleado a cargo
        self.gerente.asignar_empleado(self.empleado)
        self.assertIn(self.empleado, self.gerente._empleados_a_cargo)

    def test_departamento_agregar_empleado(self):
        """Verifica la asignación de empleados a un departamento."""
        depto = Departamento(1, "Ingeniería", self.gerente)
        depto.agregar_empleado(self.empleado)

        self.assertEqual(len(depto.empleados), 1)
        self.assertIn(self.empleado, depto.empleados)

    def test_calculo_costo_registro_tiempo(self):
        """Verifica el cálculo del costo laboral en un registro de tiempo."""
        horas = 8.0
        registro = RegistroTiempo(1, self.empleado, self.proyecto, horas)

        costo_esperado = horas * self.empleado.tarifa_hora  # 8 * 25.0 = 200.0
        self.assertEqual(registro.calcular_costo_laboral(), costo_esperado)

    def test_registro_tiempo_horas_invalidas(self):
        """Verifica que no se permitan horas negativas o en cero."""
        with self.assertRaises(ValueError):
            RegistroTiempo(2, self.empleado, self.proyecto, -5.0)


if __name__ == "__main__":
    unittest.main()